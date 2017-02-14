from pytest import fixture
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


# Adapted from
# http://www.axelspringerideas.de/blog/index.php/2016/08/16/continuously-delivering-infrastructure-part-1-ansible-molecule-and-testinfra/
#
# This is a little fancy for my taste. pytest fixtures are cool -- they're how
# the testinfra File and Package helpers are implemented, so I think the author
# was aiming for consistency -- but I'm not sure this one improves readability
# or maintainability. However, 1) I didn't have to write it and 2) I thought it
# might be instructive to show this approach. Contrast with the more direct
# approach I use in test_influxdb_repo_key_is_installed().
@fixture()
def Repository_exists(Command):
    """
    Tests if YUM Repo with specific Name exists and is enabled:
    - **repo** - repo name to look for
    **returns** - True if String is found
    """
    def f(repo):
        return (repo in Command.check_output("yum repolist"))
    return f


def test_influxdb_repo_is_installed(Repository_exists):
    assert Repository_exists("Influxdb upstream yum repo")


def test_influxdb_repo_key_is_installed(Command):
    # Adapted from https://wiki.centos.org/TipsAndTricks/YumAndRPM:
    # Show all installed GPG keys
    # Thanks to forum user babo for this one-liner to show all GPG keys along
    # with the corresponding repo information.
    rpm_keys = Command.check_output("rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'")
    assert "influxdb" in rpm_keys


def test_influxdb_package_is_installed(Package):
    pkg = Package("influxdb")
    assert pkg.is_installed


def test_which_package_is_installed(Package):
    pkg = Package("which")
    assert pkg.is_installed


# Influxdb will install a sysvinit script if it can't find systemd. Since we
# want it to find systemd, insist that the legacy sysvinit script is not
# installed.
def test_etc_initd_influxdb_is_not_installed(File):
    sysvinit = File("/etc/init.d/influxdb")
    assert not sysvinit.exists


def test_influxdb_config_has_collectd_enabled(File):
    config = File("/etc/influxdb/influxdb.conf").content_string
    assert "# BEGIN ANSIBLE MANAGED BLOCK" in config


def test_influxdb_has_collectd_database(Command):
    databases = Command.check_output("influx -execute 'show databases'")
    assert "collectd" in databases

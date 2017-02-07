from pytest import fixture
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


# Adapted from
# http://www.axelspringerideas.de/blog/index.php/2016/08/16/continuously-delivering-infrastructure-part-1-ansible-molecule-and-testinfra/
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


def test_infludb_repo_key_is_installed_(Command):
    # Adapted from https://wiki.centos.org/TipsAndTricks/YumAndRPM:
    # Show all installed GPG keys
    # Thanks to forum user babo for this one-liner to show all GPG keys along
    # with the corresponding repo information.
    rpm_keys = Command.check_output("rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'")
    assert "influxdb" in rpm_keys


def test_influxdb_package_is_installed(Package):
    pkg = Package("influxdb")
    assert pkg.is_installed


def test_influxdb_config_has_collectd_enabled(File):
    config = File("/etc/influxdb/influxdb.conf").content_string
    assert "[[collectd]]\n  enabled = true" in config

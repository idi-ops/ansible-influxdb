Ansible role: influxdb
=========

Minimal Ansible role to manage influxdb on CentOS 7.3.

Requirements
------------

 * CentOS 7.x
 * Ansible 2.x
 * systemd

Role Variables
--------------

```
influxdb_config_file: /etc/influxdb/influxdb.conf

influxdb_packages:
- influxdb
- which

# e.g. /centos/7/x86_64/stable/
influxdb_repo: https://repos.influxdata.com/centos/$releasever/$basearch/stable/

influxdb_repo_key: https://repos.influxdata.com/influxdb.key
```

Dependencies
------------

 * ansible-collectd - https://github.com/idi-ops/ansible-collectd

Example Playbook
----------------

    - hosts: servers
      roles:
         - ansible-influxdb
           influxdb_package_version: 1.2.0

Tests
-----

Use [molecule](https://github.com/metacloud/molecule) to test this role.

Because this role depends on systemd and SELinux, only a Vagrant provider is configured at the moment.

License
-------

MIT

Author Information
------------------

Raising the Floor - US

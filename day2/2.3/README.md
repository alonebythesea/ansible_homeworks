# Working with Roles - Practice

## Create Following Roles:


<details><summary>base</summary>

A role which configures system defaults:
  - installs (for example) `epel-release`, `python`, `pip`, `curl`, `wget`, `sudo`, `iproute` and other packages
  - ensures that ansible facts folder exists
  - discovers ansible facts (use **explicit** behaviour and gather all facts here)
  - etc
</details>



<details><summary>user</summary>

A role which creates system user, accepts following arguments:
  - `user_name`/`user_id`
  - `user_group`/`user_gid` (dafault to `user_name`/`user_id`)
  - `user_sudo_privs` (for example: `ALL=(ALL) NOPASSWD:ALL`, default empty - means no sudo privileges provided to current user), use `validate` command to test sudoers configuration changes before apply
  - `user_home` - default to `/home/{{ user_name }}`
  - `user_home_create` - default to `true`
  - `user_shell` default to `/bin/sh`
</details>

<details><summary>webapp-server</summary>

A role (rework playbook from previous homework) which installs application service and accepts following parameters (at least):

  - `webapp_server_user` - calls `user` role with this argument
  - `webapp_server_group` (default to `webapp_server_user`)
  - `webapp_server_home` - varaible for application home folder (example: `/opt/webapp-server/`)
  - `webapp_server_port` - application port (default to `8080`)
  - `webapp_server_bin_url` - app binary file (default to `https://playpit-labs-assets.s3-eu-west-1.amazonaws.com/webapp-server/webapp-server`)
  - `webapp_server_logo_url` choose any for default
  - `webapp_server_student_name` - web page message (with `student_first_name` and `student_last_name` variables, from play vars)
</details>

<details><summary>mysql_db</summary>

A role which installs MySQL DB:

  - https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html
  - https://dev.mysql.com/doc/refman/8.0/en/data-directory-initialization.html
  - https://chartio.com/resources/tutorials/how-to-grant-all-privileges-on-a-database-in-mysql/
  - define db's `root` password on Playbook level and treat in as mandatory in a role
  - installation details (shell way):
      1. rpm -Uvh https://repo.mysql.com/mysql80-community-release-el7-3.noarch.rpm
      2. yum --enablerepo=mysql80-community install mysql-community-server
      3. mysqld --initialize-insecure --user=mysql
      4. systemctl enable --now mysqld
      5. echo "ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';" | mysql -u root --skip-password
  - use "change control" to consider if configuration item changed or not
  - define variable `mysqldb_root_password` defaults `root`)
</details>

<details><summary>mysql_db_user</summary>

A role which creates MySQL user:

  - https://www.inmotionhosting.com/support/website/how-to-create-a-database-using-mysql-from-the-command-line/
  - https://docs.ansible.com/ansible/2.9/modules/list_of_database_modules.html#mysql
  - define and use variables like `mysqldb_user`, `mysqldb_password`, `mysqldb_database`
</details>

<details><summary>mysql_db_check</summary>

A role is an ui for verifying connectivity to db:

  - define role variables, for example:
    - `mysqldb_check_user` (default to `mysqldb-check`
    - `mysqldb_check_group` (default to `mysqldb_check_user` variable)
    - `mysqldb_check_home` (default to `/opt/mysqldb-check`)
    - `mysqldb_check_port` (default to `8080`)
    - `mysqldb_check_bin_url` (default to `https://playpit-labs-assets.s3-eu-west-1.amazonaws.com/mysql-check/mysql-check`)
  - create folders under `{{ mysqldb_check_home }}`:
      - `bin/`
      - `config/`
  - download binary to `bin/`
  - create config file with just `PORT={{ mysqldb_check_port }}` line, copy it under `config/` folder
  - configure `mysqldb-check.service`
  - configure system user for running this service
</details>

### Create Hosts Inventory

Create an inventory file (`./inventory`):

- Specify group(s): `appservers`, `dbservers`
- Specify group variables
- Specify remote host(s) (`ip` or `fqnd`)
- Specify host alias (for example: `db1`)
- Specify connection parameters (at least):
  - set `ansible_user`
  - set `ansible_private_key_file`
- Use variables grouping

### Create Playbooks for Testing These Roles:

- `role-base.yml` (hosts: all)
- `role-mysqldb.yml` (hosts: dbservers)
- `role-mysqldb-check.yml` (hosts: appservers)
- `role-user.yml` (hosts: appservers)
- `role-webapp-server.yml` (hosts: appservers)

I want to see all your use cases, how you test these roles.

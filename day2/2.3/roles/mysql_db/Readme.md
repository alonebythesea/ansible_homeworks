# `mysql_db`** Role

## It installs MySQL DB Server

Please find instructions how to do it manually:

- https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html
- https://dev.mysql.com/doc/refman/8.0/en/data-directory-initialization.html
- https://chartio.com/resources/tutorials/how-to-grant-all-privileges-on-a-database-in-mysql/
- define db's `root` password on Playbook level and treat in as mandatory in a role
- installation details (shell way):
    1. rpm -Uvh https://repo.mysql.com/mysql80-community-release-el7-3.noarch.rpm
    2. yum --enablerepo=mysql80-community install mysql-community-server
    3. mysqld --initialize-insecure --user=mysql
    4. systemctl enable --now mysqld
    5. echo "ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';" | mysql

Role's Specification:

- use "change control" to consider if configuration item changed or not
- define variable `mysqldb_root_password` defaults `root`

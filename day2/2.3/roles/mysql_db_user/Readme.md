# `mysql_db_user` Role

## It creates MySQL user

- https://www.inmotionhosting.com/support/website/how-to-create-a-database-using-mysql-from-the-command-line/
- https://docs.ansible.com/ansible/2.9/modules/list_of_database_modules.html#mysql
- define and use variables like `mysqldb_user`, `mysqldb_password`, `mysqldb_database`

This role requires to know `root`'s credentials, therefore please pass `mysqldb_root_password`

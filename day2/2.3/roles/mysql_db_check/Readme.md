# `mysql_db_check` Role

## It is an UI for verifying connectivity to db:

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

# `webapp-server` Role

## It installs application service and accepts following parameters (at least):

- `webapp_server_user` - calls `user` role with this argument
- `webapp_server_group` (default to `webapp_server_user`)
- `webapp_server_home` - varaible for application home folder (example: `/opt/webapp-server/`)
- `webapp_server_port` - application port (default to `8080`)
- `webapp_server_logo_url` choose any for default
- `webapp_server_student_name` - web page message with your name

# `user`** Role

## It creates OS users, accepts following arguments:

- `user_name`/`user_id`
- `user_group`/`user_gid` (dafault to `user_name`/`user_id`)
- `user_sudo_privs` (for example: `ALL=(ALL) NOPASSWD:ALL`, default empty - means no sudo privileges provided to current user), use `validate` command to test sudoers configuration changes before apply
- `user_home` - default to `/home/{{ user_name }}`
- `user_home_create` - default to `true`
- `user_shell` default to `/bin/sh`

All other roles should use this role as dependent

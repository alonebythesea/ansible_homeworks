# Ansible Day 1: Creating Own Playbook

### Configure Remote Connection

Assuming you can connect to the remote vm under `root` (or any other privileged user) and you are going to create `devops:devops` user on the target:

- using ansible ad hoc command, create user (`devops:devops`) on the target machine
- run command as following: `ansible {remote-vm} -i {inventory} -u {root} -k -m user -a "... arguments ..."`
- configure sudoers privileges for nearly created user: `ansible {remote-vm} -i inventory -u {root} -k -m copy -a "src=devops.sudoers dest=/etc/sudoers.d/devops"`
- add public key into authorised keys: `ansible {remote-vm} -i inventory -u {root} -k -m authorized_key -a "..."`

Once all of these done, please check connectivity using `devops` user:
- update inventory file with necessary settings (save original inventory file to `inventory.orig`)
- run a command like this one: `ansible all -i inventory -m ping`, there should be `pong`
and no connectivity issues.

### Playbook Requirements:

Create `webapp-server.yml` playbook. I should do following:

- create application user/group (for example: `webapp-server:webapp-server`, service `webapp-server` should run under this user)
- create application folders (`file` module)
- make sure all resources belong to application user: `/opt/webapp-server/bin/` and `/opt/webapp-server/conf/`
- download (`get_url`) executable file (https://playpit-labs-assets.s3-eu-west-1.amazonaws.com/webapp-server/webapp-server), checksum=??? (find it and set!)
- copy configuration file to `/opt/webapp-server/conf/webapp-server.conf`
- copy systemd unit file from control machine to the target (`copy`)
- register systemd service as `webapp-server`, enable and start application service (`systemd`)
- use privilege escalation (`become`/`become_user`) where it's required
- use ansible `handlers` to make sure that app service is restarted once any of dependent configuration changed (settings applied)
- provide all tasks with `name` parameter and describe the purpose of this task
- USE VARIABLES!

Following variables should be defined and used:
- `webapp_user`
- `webapp_group`
- `webapp_url`
- `webapp_home`
- `student_first_name`
- `student_last_name`

Following Resources should be created (make templates from them) and used:

<details><summary>webapp-server.conf.j2</summary>

```ini
port=8080
message=Done by Ansible
name={student_first_name} {student_last_name}
logo_url=https://playpit-labs-assets.s3-eu-west-1.amazonaws.com/images/Ansible_logo.svg.png
logo_height=60
```
</details>

<details><summary>webapp-server.service.j2</summary>

```ini
[Unit]
Description=Simple WebApp Server
After=network.target

[Service]
Type=simple
EnvironmentFile=-/opt/webapp-server/conf/webapp-server.conf
ExecStart=/opt/webapp-server/bin/webapp-server
ExecStop=/bin/kill -s QUIT $MAINPID

[Install]
WantedBy=multi-user.target
```
</details>

### Add your Host into `inventory` file

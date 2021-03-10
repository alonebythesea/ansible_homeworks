# Ansible Day 1: Getting Familiar with Ansible Framework

## 1. Developing Ansible Playbook:

#### 1.1 Use variables instead of `???`
#### 1.2 Improve this playbook to be fully idempotent! (Don't delete tasks)
#### 1.3 Make sure It can run from non-root user

<details><summary>./tomcat.yml</summary>

```yaml
- name: Installing Tomcat
  hosts: app-server

  vars:
    tomcat_user: tomcat
    tomcat_group: tomcat

    tomcat_version: 8.5.58
    tomcat_version_major: "{{ tomcat_version.split('.')[0] }}"

    tomcat_url: https://archive.apache.org/dist/tomcat/tomcat-{{ tomcat_version_major }}/v{{ tomcat_version }}/bin/apache-tomcat-{{ tomcat_version }}.tar.gz
    tomcat_home: /usr/share/tomcat

    tomcat_admin_username: admin
    tomcat_admin_password: password

  tasks:
  - name: Install Java 1.8
    yum: name=java-1.8.0-openjdk state=present

  - name: Create tomcat Group
    group:
      name: ???

  - name: Add user "tomcat"
    user:
      name: ???
      group: ???
      home: ???
      createhome: no

  - name: Download Tomcat
    get_url:
      url: ???
      dest: /opt/apache-tomcat-???.tar.gz
      checksum: "md5:9def3ec8010601a837373a1754e97d9d"

  - name: Unpack Tomcat Archive
    unarchive:
      src: /opt/apache-tomcat-???.tar.gz
      dest: /opt/
      remote_src: yes
      owner: ???
      group: ???
      creates: /opt/apache-tomcat-???/conf/tomcat-users.xml

  - name: Symlink install directory
    file:
      src: /opt/apache-tomcat-???
      path: ???
      state: link

  - name: Copy Users Configuration
    template:
      src: tomcat-users.xml.j2
      dest: /opt/apache-tomcat-???/conf/tomcat-users.xml
      owner: ???
      group: ???
    notify: tomcat restart

  - name: Disable Manager Access Restrictions
    replace:
      path: "???/webapps/manager/META-INF/context.xml"
      regexp: (\s\+<)(Valve[^>]*/)>
      replace: \1!--\2--
      backup: yes

  - name: Copy Tomcat Service File
    template:
      src: tomcat.service.j2
      dest: /usr/lib/systemd/system/tomcat.service

  - name: Ensure Tomcat Service Enabled and Running
    systemd:
      name: tomcat
      state: started
      enabled: yes

  handlers:
  - name: tomcat restart
    systemd:
      name: tomcat
      state: restarted
```
</details>

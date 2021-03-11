#!/usr/bin/python


DOCUMENTATION = '''
---
module: wget
short_description: Just downloads tomcat with given arguments
options:
    "src"      (mandatory)(provided by filter), src location of tomcat(provided by filter)
    "dest"     (mandatory), destination folder for download
    "checksum" (optional)(may be provided by filter), checksum to compare(available checksums are md5, sha1, sha256, sha384, sha512)
    "group"    (optional), set group who owns downloaded file
    "owner"    (optional), set user who owns  downloaded file
    "mode"     (optional), set permissions for the downloaded file
'''

EXAMPLES = '''
vars:
    tomcat_version = 8.5.58
tasks:
  - name: Download tomcat
    wget:
      src: "{{ tomcat_version | tomcat_url }}"
      dest: /opt
      checksum: "{{ tomcat_version | tomcat_checksum }}"
      group: root
      owner: root
      mode: 0755
    become: true
'''


from ansible.module_utils.basic import *
import os
import hashlib
import urllib.request
import pwd
import grp


def main():

    module = AnsibleModule(
    argument_spec=dict(
        src=dict(requred=True),
        dest=dict(required=True),
        checksum=dict(required=False, aliases=['chcksum', 'chksum']),
        group=dict(required=False),
        owner=dict(required=False),
        mode=dict(required=False)
        ))

    src = module.params["src"]
    dest = module.params["dest"]
    checksum = module.params["checksum"]
    group = module.params["group"]
    owner = module.params["owner"]
    mode = module.params["mode"]

    changed = False
    tomcat_downloaded = False
    owner_changed = False
    group_changed = False
    mode_changed = False

    if fun_get_tomcat(src, dest):
        changed = True
        tomcat_downloaded = True

    if checksum:
        if not fun_check_checksum(filename, checksum):
            module.fail_json(msg="Checksums don't match!")

    if owner:
        if fun_owner(filename, owner):
            changed = True
            owner_changed = True

    if group:
        if fun_group(filename, group):
            changed = True
            group_changed = True

    if mode:
        if fun_mode(filename, mode):
            changed = True
            mode_changed = True

    change_state = {
            'src': mode,
            'chksum': checksum,
            'group': group,
            'owner': owner,
            'mode': mode
            }

    module.exit_json(changed=changed, **change_state)


def fun_parse_version(src):
    version = src.split('/v')[1]
    version = version.split('/b')[0]
    return version


def fun_dest(dest):
    if not os.path.exists(dest):
        os.makedir(dest)
    return dest


def fun_get_tomcat(src, dest):
    version = fun_parse_version(src)
    destination = fun_dest(dest)
    global filename
    filename = destination + '/apache-tomcat-' + version + '.tar.gz'
    check = os.path.exists(filename)
    if not check:
        urllib.request.urlretrieve(src, filename)
        return True
    else:
        return False

def fun_check_checksum(filename, checksum):
    checksum_type = checksum.split(":")[0]
    checksum_value = checksum.split(":")[1] 
    with open(filename, 'rb') as f:
        if checksum_type == "md5":
            m = hashlib.md5()
        elif checksum_type == "sha1":
            m = hashlib.sha1()
        elif checksum_type == "sha256":
            m = hashlib.sha256()
        elif checksum_type == "sha384":
            m = hashlib.sha384()
        elif checksum_type == "sha512":
            m = hashlib.sha512()
        while True: 
            data = f.read(2**20)
            if not data:
                break
            m.update(data)
        f.close()
        hex_val = m.hexdigest()
    return checksum_value == hex_val 
 

def fun_group(filename, group):
    try:
        grp.getgrnam(group)
        gid = grp.getgrnam(group).gr_gid
        current_group = os.stat(filename).st_gid
    except Exception:
        module.fail_json(msg="Group does not exist!")
    uid = -1
    if current_group == gid:
        return False
    else:
        os.chown(filename, uid, gid)
        return True


def fun_owner(filename, owner):
    try:
        pwd.getpwnam(owner)
        uid = pwd.getpwnam(owner).pw_uid
        current_owner = os.stat(filename).st_uid
    except Exception:
        module.fail_json(msg="User does not exist!")
    gid = -1
    if current_owner == uid:
        return False
    else:
        os.chown(filename, uid, gid)
        return True


def fun_mode(filename, mode):
    st = os.stat(filename)
    current_mode = oct(st.st_mode)[-4:]
    current_mode = int(current_mode, 8)
    mode = oct(int(mode))
    mode = int(mode, 8)
    if current_mode == mode:
        return False
    else:
        os.chmod(filename, mode)
        return True


if __name__ == '__main__':
    main()

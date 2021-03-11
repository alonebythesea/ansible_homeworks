# Ansible Day 3: Extending Ansible with Custom Filters and Modules

## 1. Extending Ansible with Custom Filters

### Custom filter `tomcat_url`

The `tomcat_url` filter should generate url for getting tar.gz archive:

```
- hosts: remotevm
  
  vars:
    tomcat_version: 9.0.27
  
  tasks:
  - debug: msg="{{ tomcat_version | tomcat_url }}"
    # produces:  https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.27/bin/apache-tomcat-9.0.27.tar.gz
```

If there's no url by requested version, the filter should return "none" string

### Custom filter `tomcat_checksum`

The idea of using this filter is shown below:
```
- name: Trying Tomcat v8.0.12
  hosts: remotevm
  
  vars:
    tomcat_version: 8.0.12
  
  tasks:
  - debug: msg="{{ tomcat_version | tomcat_url }}" 
    # produces: https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.12/bin/apache-tomcat-8.0.12.tar.gz

  - debug: msg="{{ tomcat_version | tomcat_checksum }}" 
    # produces: md5:2209cf269a1e73f2fd5f451a3703afbc

- name: Trying Tomcat v8.5.39
  hosts: remotevm
  
  vars:
    tomcat_version: 8.5.39
  
  tasks:
  - debug: msg="{{ tomcat_version | tomcat_url }}" 
    # produces: https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.39/bin/apache-tomcat-8.5.39.tar.gz

  - debug: msg="{{ tomcat_version | tomcat_checksum }}" 
    # produces: sha512:8396f526eca9b691931cfa773f43c5190e7002d938cb253335b65a32c7ef8acba2bf7c61f2ccffc4113a3ba0c46169a4e4797cdea73db32c5ba56156a9f49353
```

This filter should try `md5`, `sha1`, `sha256`, `sha384` or `sha512`files and figure out what is available.

### Create "Testing" playbook

Create `testing-my-filters.yml` playbook. It should have several cases and use `assert` module to test them.

## 2. Extending Ansible with Custom Module

### Develop `wget` module

Create folder `./library` and place your code over there

Module works similar to `get_url`, accepts following parameters (get parameters description from `ansible-doc get_url`):

- src (=)
- dest (=)
- chksum (-)
- group (-)
- owner (-)
- mode (-)

Example:
```yaml
- hosts: remotevm
  
  vars:
    tomcat_version: 8.5.39

  tasks:
    - name: Download Tomcat Archive
      wget:
        src: "{{ tomcat_version | tomcat_url }}"
        chksum: "{{ tomcat_version | tomcat_checksum }}"
        dest: /opt # it's a folder!
        group: tomcat
        owner: tomcat
        mode: 0644
```

If there's no such file (by url) module should fail with the message "Cand find requested file! URL is: {{ url }}"

### Difference with `get_url` module

Original `get_url` module **always** downloads remote file, checks `checksum` - but only for validating downloaded file. We'd like to use this `checksum` for checking a file `dest` directory first, and **only** if it differs, it will proceed with downloading (performing update)

### Document this Module

```
ansible-doc wget -M path/to/custom/modules/
```

### Add ansible adhoc commads for testing your module:

```
## add commands and outputs here:
```

### Add your tast cases into `testing-wget-module.yml` playbook


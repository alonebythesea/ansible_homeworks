# Asnible Day 3: Loops, Filters, Jinja2 Templates

## Practicing Jinja2

<details><summary>users files ./vars/users-ccl-team.yml</summary>

```yaml
tomcat_users:

- name: beth
  role: manager-gui
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      36653964613436363662626331663963373962616566633533386237613234396338646232383733
      3236646334623935653662373234353266313432353830310a623030303139396462363637326430
      64313631616665303964323063346638393264353935623039393932666637306663633665633335
      3863316461623837390a613333356663343130346161356239653262346234396363363761663465
      6431

- name: lora
  role: manager-script
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      33653265316464323666633237353238383033616433613863373839393530323363353363326139
      3333373338626335356362386264643336626339316133330a343038336136306564623534396631
      65666263653731656639383539373636336461343237393732643762393666613836616466633461
      3366663231376635660a636464306263396430353631633434313164613339636336363735613033
      3331
```
</details>

<details><summary>users files ./vars/users-pgwy-team.yml</summary>

```yaml
tomcat_users:

- name: simon
  role: manager-gui
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      65326534613163666134643130643330343766623564393435303631383932653032366334373932
      6634336536333035383065316536383565333964393633660a393034363065363435616162366637
      33643530363364393662323837633838353232323364313636613935623465643762393237623865
      6637363037623963370a366436656566363862643436333135376333383139323934666461636466
      3739

- name: pablo
  role: manager-gui
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      62333962313831333632303033326363666462383464646433366464663361323839303666643939
      3332353366393739366362353065653735313866303437330a326364666239643463393535616138
      32396663663937356435613135663766623862393935643264626231633662383531383739626637
      6464393465323838390a623039303930656231333034646563353135636361323465306639353233
      6237

- name: mark
  role: manager-gui
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      62626430366231616466356334623235323431343334326561646534363265626430393861373936
      6563656562613962323536323338663634393765376366330a306139326163373066623635376532
      33366234366666666432656365326331656535353563323364366637396662626664343132373336
      6432613437303265340a343039646639613730613963323661636139323538653461366333343661
      6330

- name: babash
  role: manager-script
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      66376438366630303938353564666361653862636639663561393035656537336333363033393361
      6130633739636531363964376137393261656633636265300a626366303338323636363262383237
      36613632373066393264323762313536653035623532326633376537393161343239353430666535
      3466373635626233300a303462313463383837643136393337663466333936653339633237313933
      6436

- name: olaf
  role: manager-script
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      34303964336161336133353132666266656633636163616536303566336232336538393735663437
      3461616665363262656631306332666466643664623135390a646531323562333063373065666236
      63656562626163363966333930616463396665323436643539633665316335323063363831396239
      3061623466373664300a353435366132363961616563333061323237396337373034326661336534
      3235

- name: charley
  role: manager-status
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      65363865666536353432316261303162386637373661313639626362626232623033366134336236
      3862386361323966303436346363663834313139303333640a626135626138333764623335313637
      30373965343633313462313564613436393734333530303863613036346133363162313164626437
      6431333065313337660a366663636533303932643161396463623437356238383439356436336133
      3738

- name: roxie
  role: manager-status
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      36656434306136363362333531326365636331316436643066663430336239323861323464636437
      6663363735313161663934663866303439636130623239630a336238633535616166313862383433
      62306163356338373233376561643234663338383537383732373535343436633139666561636365
      6133613839663034300a666433636531363563616339393630313932383333363863306535303732
      3536

- name: annabell
  role: manager-jmx
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      64316439373832623839396137376637366435353138373530653364323137636130616432646661
      3664383265613763383331333931366532663865303338370a653965633831383239623666613738
      66343333396530636666663634353538653563386464616139316665613933346166313265663261
      3831646562616336320a396631303037653164323061613431643736626239353130386335666537
      6635

- name: karl
  role: manager-jmx
  password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      36656664613930386638383436363038616262343866393033643334333631623930383936643631
      6165633134383335646339643437306630363864333739330a383635326630303332333062326164
      64376666613437393562376139326439333433363662376164353632303531306463653532306139
      3031633161356537330a663139323764643535366166323464623938333537393663313338613139
      3936
```
</details>


playbook file:

<details><summary>data-rendering.yml</summary>

```yaml
- hosts: all
  connection: local
  gather_facts: no

  tasks:
    - name: Mandatory Variable should be provided
      assert:
        that:
          - team_name is defined
          - team_name | length > 0
        msg: "Please specify 'team_name' variable"

    - name: Pass if team_name is correct
      fail:
        msg: team name should correspond to pattern '(fft|ccl|pgwy)-team'
      when: not team_name | mandatory is match('^(fft|ccl|pgwy)-team$')

    - name: Pass if variables file exists
      fail:
        msg: variables file 'vars/users-{{ team_name }}.yml' doesnt exist
      when: not path is exists
      vars:
        path: "vars/users-{{ team_name }}.yml"

    - name: Including Team Vars
      include_vars: vars/users-{{ team_name | mandatory }}.yml

    - name: Walk through users
      debug: msg="{{ user.name}} / {{ user.role }} / {{ user.password }}"
      loop: "{{ tomcat_users }}"
      loop_control:
        loop_var: user
        label: "{{ user.name }}"

    - name: Rendering Templates
      template:
        src: tomcat-users.xml.j2
        dest: tomcat_users-rendered.xml
      vars:
        users: "{{ tomcat_users }}"
```

Sample output of "Walk through users" task:
```
TASK [Walk through users] ************************************************************
ok: [here] => (item=beth) => {
    "msg": "beth / manager-gui / ..."
}
ok: [here] => (item=lora) => {
    "msg": "lora / manager-script / ..."
}
```

</details>

<details><summary>template ./templates/tomcat-users.xml.j2</summary>

Add necessary instructions so that this template produces files from examples below:
```xml
<?xml version="1.0" encoding="UTF-8"?>

{{ team_name ??? }}

<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
  <role rolename="manager-gui"/>
  <role rolename="manager-script"/>
  <role rolename="manager-status"/>
  <role rolename="manager-jmx"/>

  ???

</tomcat-users>
```
</details>

Run playbook:
```
ansible-playbook tomcat-template-rendering.yml --vault-id password -i remotevm, -e team_name=pgwy-team
ansible-playbook tomcat-template-rendering.yml --vault-id password -i remotevm, -e team_name=ccl-team
```

<details><summary>Try for "fft-team"</summary>

```
ansible-playbook tomcat-template-rendering.yml -v -i here, --vault-id=password -e team_name=fft-team
No config file found; using defaults

PLAY [all] *************************************************************************************************

TASK [Pass if team_name is correct] ************************************************************************
skipping: [here] => {"changed": false, "skip_reason": "Conditional result was False"}

TASK [Pass if variables file exists] ***********************************************************************
fatal: [here]: FAILED! => {"changed": false, "msg": "variables file 'vars/users-fft-team.yml' doesnt exist"}

PLAY RECAP *************************************************************************************************
here                 : ok=0    changed=0    unreachable=0    failed=1    skipped=1    rescued=0    ignored=0   
```
</details>

<details><summary>Rendered file example:</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>

<!--
 -
 - ccl-team
 -
-->

<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
  <role rolename="manager-gui"/>
  <role rolename="manager-script"/>
  <role rolename="manager-status"/>
  <role rolename="manager-jmx"/>

  <user username="beth" password="seeCho1O" roles="manager-gui" />
  <user username="lora" password="aixahV0i" roles="manager-script" />
</tomcat-users>
```
</details>

## 2. Ansible Filters and Data Manipulation

### Fill the gaps

<details><summary>./filters.yml</summary>

```yaml
- hosts: remotevm
  gather_facts: no

  vars:
    student_name: Mickey Mouse
    random_value: "{{ ... }}" # random number 1..100 (not 0..99!)

    profile:
      firstname: Joe
      lastname: Doe
      age: 32
      skills:
        - Ansible
        - Docker
        - Kubernetes

  tasks:
    - name: Should be "mickey mouse"
      debug: msg="{{ student_name | ... }}"

    - name: Should be "Name - Mickey, Surname - Mouse"
      debug: msg="{{ ... student_name ... }}"

    - name: Should be "Mickey MOUSE"
      debug: msg="{{ ... student_name ... }}"

    - name: Should be "Minnie Mouse"
      debug: msg="{{ student_name ... }}"

    - name: Testcase with assert module and random_value
      assert:
        that:
          - 'random_value ... <= 100'
          - 'random_value ... >= 1'
        msg: "'random_value' must be between 1 and 100"

    - name: Save profile variable in Json file (one line)
      copy:
        content: "{{ profile ... }}"
        dest: profile.json

    - name: Should be in Json format (one line)
      debug: msg="{{ profile ... }}"
      register: string_value

    - name: Save profile variable in Json file (multiple lines, indentation)
      copy:
        content: "{{ profile ... }}"
        dest: profile_pretty.json

    - name: Should be in Json format (multiple lines, indentation)
      debug: msg="{{ profile ... }}"

    - name: Create dict variable from string value
      set_fact: nearly_created="{{ string_value.msg ... }}"

    - name: Testcase with assert module and nearly_created variable
      assert:
        that:
          - 'nearly_created.firstname == "..."'
          - 'nearly_created.lastname == "..."'
          - 'nearly_created.age == 32'

    - name: Encode with base64 sensitive data
      debug: msg="{{ 'too sensitive to be plain' | ... }}"

    - name: Decode Base64 encoded string
      debug: msg="{{ 'QWxtaWdodHkgQW5zaWJsZSE=' | ... }}"
```
</details>

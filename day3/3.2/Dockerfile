FROM centos:8

RUN yum install python3-pip -y && \
pip3 install cryptography==3.2 && \
pip3 install ansible

RUN ansible --version

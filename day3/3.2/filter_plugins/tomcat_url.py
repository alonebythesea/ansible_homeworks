#!/usr/bin/python


import urllib.request
from urllib.parse import urlparse


class FilterModule(object):
    def filters(self):
        return {
            'tomcat_url': self.tomcat_url,
            'tomcat_checksum': self.tomcat_checksum
        }


    def tomcat_url(self, tomcat_version):
        tomcat_major = tomcat_version.split('.')[0]
        url = 'https://archive.apache.org/dist/tomcat/tomcat-' + tomcat_major +\
            '/v' + tomcat_version + '/bin/apache-tomcat-' + tomcat_version + '.tar.gz'
        try:
            check_url_code = urllib.request.urlopen(url).getcode()
            if check_url_code == 200:
                return url
        except Exception:
            return "none"


    def tomcat_checksum(self, tomcat_version):
        tomcat_major = tomcat_version.split('.')[0]
        url = self.tomcat_url(tomcat_version) 
        checksums = ['md5', 'sha1', 'sha256', 'sha384', 'sha512']
        if url == "none":
            return "none"
        else:
            for i in checksums:
                try:
                    check_url = url + '.' + i
                    check_code = urllib.request.urlopen(check_url).getcode()
                    if check_code == 200:
                        valid_checksum = i
                        valid_url = check_url
                        parse = urllib.request.urlopen(valid_url)
                        parsed = parse.read()
                        parsed = parsed.decode('utf-8')
                        parsed = valid_checksum + ':' + parsed.split(' ')[0]
                        return parsed
                except Exception:
                    continue

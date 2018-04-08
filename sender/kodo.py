#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import qiniu
import ConfigParser


class Kodo(object):
    def __init__(self, cf):
        try:
            ak = cf.get('sender_kodo', 'ak')
        except ConfigParser.NoSectionError:
            raise Exception('ak is empty')
        except ConfigParser.NoOptionError:
            raise Exception('ak is empty')
        try:
            sk = cf.get('sender_kodo', 'sk')
        except ConfigParser.NoSectionError:
            raise Exception('sk is empty')
        except ConfigParser.NoOptionError:
            raise Exception('sk is empty')
        try:
            bucket = cf.get('sender_kodo', 'bucket')
        except ConfigParser.NoSectionError:
            raise Exception('bucket is empty')
        except ConfigParser.NoOptionError:
            raise Exception('bucket is empty')
        self.bucket = bucket
        self.q = qiniu.Auth(ak, sk)

    def _prepare(self, file_name):
        self.token = self.q.upload_token(self.bucket, file_name, 3600*24*365*100)

    def _put_file(self, file_path, file_name):
        print 'begin to send file %s' % (file_name, )
        ret, info = qiniu.put_file(self.token, file_name, file_path)
        if info.status_code == 200:
            assert ret['key'] == file_name
            assert ret['hash'] == qiniu.etag(file_path)
            print 'send file %s finished' % (file_name, )
        else:
            print 'send file %s error' % (file_name, )
            print 'response is', info

    def main(self, file_path):
        file_name = os.path.basename(file_path)
        self._prepare(file_name)
        self._put_file(file_path, file_name)

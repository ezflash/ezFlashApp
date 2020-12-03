# The MIT License (MIT)
# Copyright (c) 2019 ezflash
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import os
import boto3
import botocore

import pyupdater.cli as pyucli

import argparse
import threading
import sys
import platform

SRC_FOLDER = os.path.join('pyu-data','deploy')

from autoUpdate import APP_NAME

BUCKET_NAME = 'update.ezflash.org' # replace with your bucket name
FOLDER_NAME = APP_NAME

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s / %s  (%.2f%%)" % (self._seen_so_far,
                                         self._size, percentage))
            sys.stdout.flush()


class  release():

    def __init__(self,args):

        self.version = args.app_version
        print("Release version {}".format(self.version))


        fp = open('app_version.py','w')
        fp.write('APP_VERSION=\"{}\"'.format(self.version))
        fp.close()

        if args.operation in 'all':
            self.build()
            self.package()
            self.upload()
        elif args.operation in 'dmg':
            self.dmg()
        elif args.operation in 'build':
            self.build()
        elif args.operation in 'package':
            self.package()
        elif args.operation in 'upload':
            self.upload()






    def upload(self):      

        print("Start upload")  
        fileList = [f for f in os.listdir(SRC_FOLDER) if os.path.isfile(os.path.join(SRC_FOLDER, f))]
        s3 = boto3.client('s3')

        for f in fileList:
            try:
                print("Upload {}".format(f))
                s3.upload_file(os.path.join(SRC_FOLDER,f),BUCKET_NAME,'{}/{}'.format(FOLDER_NAME,f),ExtraArgs={'ACL': 'public-read'},
                                Callback=ProgressPercentage(os.path.join(SRC_FOLDER,f)))
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise

            print() # cariage retrun



    def build(self):
        if platform.system() == 'Windows':
            pyucli.main(['build','--app-version', self.version, 'pyu-win.spec'])

        elif platform.system() == 'Darwin':
            pyucli.main(['build','--app-version', self.version, 'pyu-mac.spec'])
            self.dmg()
        else:
            raise Exception("Unsupported platform")


    def dmg(self):
        src = os.path.join('pyu-data','new','{}.app'.format(APP_NAME))
        dst = os.path.join('pyu-data','new','{}-{}.dmg'.format(APP_NAME,self.version))
        os.system('hdiutil create {} -srcfolder {} -ov'.format(dst,src))
        



    def package(self):
         pyucli.main(['pkg','--process','--sign','--split-version'])





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Release tool')
    parser.add_argument('-a','--app-version',help='Version to release',required=True)
    subparsers = parser.add_subparsers(dest='operation',help='Run  {command} -h for additional help')

    subparsers.add_parser('all',help="build, pkg, upload")
    subparsers.add_parser('build',help="build, pkg, upload")
    subparsers.add_parser('dmg',help="make dmg")
    subparsers.add_parser('pkg',help="build, pkg, upload")
    subparsers.add_parser('upload',help="build, pkg, upload")


    args = parser.parse_args()
    release(args)
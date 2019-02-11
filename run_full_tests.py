#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import subprocess
import tempfile
import shutil


class InTempDir(object):
    def __init__(self, suffix='', prefix='tmp', directory=None, delete=True):
        self.delete = delete
        self.temp_path = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=directory)

    def __enter__(self):
        self.orig_path = os.getcwd()
        os.chdir(self.temp_path)
        return self

    def __exit__(self, *exc_info):
        # Restore the working dir and cleanup the temp one
        os.chdir(self.orig_path)
        if self.delete:
            shutil.rmtree(self.temp_path)

def test1():
    with InTempDir(prefix='scuba-systest', directory='.'):
        with open('.scuba.yml', 'w+t') as f:
            f.write('image: debian:8.2\n')

        in_data = 'success'

        with open('file.in', 'w+t') as f:
            f.write(in_data)

        subprocess.check_call(['scuba', '/bin/sh', '-c', 'cat file.in >> file.out'])

        with open('file.out', 'rt') as f:
            out_data = f.read()

        assert in_data == out_data

def main():
    test1()
    print('All is good.')

if __name__ == '__main__':
    main()

#!/usr/bin/env python

"""
Copyright 2017 ARC Centre of Excellence for Climate Systems Science
author: Aidan Heerdegen <aidan.heerdegen@anu.edu.au>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function

import hashlib
import netCDF4 as nc
import os, sys
import argparse
import re
from subprocess import check_output, CalledProcessError, STDOUT
from collections import defaultdict

class NotNetcdfFileError(Exception):
    """Exception raised when attempting to open a non-netCDF file"""

    def __init__(self, filename):
        assert filename
        self.filename = filename

    def __str__(self):
        return "{} is not a netCDF format file\n".format(self.filename)

class NCDataHash(object):
    """A hash used to uniquely identify a netCDF data file
    """

    def __init__(self, filename, noname=False, nomtime=False):
        """Return a DataHash object for filename"""
        self.stripfilename = noname
        self.ignoremtime = nomtime
        self.filename = filename

    def getmtime(self):

        # Tried using h5py to access internal mtime attribute, but
        # this is not always used, so just use modification time

        self.mtime = os.path.getmtime(self.filename) 
        return self.mtime

    def getheader(self):
        try:
            self.ncdump = check_output(["ncdump","-h",self.filename],stderr=STDOUT).decode()
        except CalledProcessError as e:
            if "NetCDF: Unknown file format" in e.output.decode():
                raise NotNetcdfFileError(self.filename)
            else:
                raise
        if self.stripfilename:
            # Strip out the filename from the ncdump header dump. This is
            # not a fundamental part of the netcdf file structure, but is
            # required to remake the file with ncgen
            self.ncdump = re.sub(r'^netcdf.*{\n','{\n',self.ncdump,1)

    def makehash(self):
        if self.ignoremtime:
            self.hashstring = str(self.size) + self.ncdump
        else:
            self.hashstring = str(self.size) + str(self.mtime) + self.ncdump
        self.md5.update(self.hashstring.encode())

    def gethash(self):
        self.md5 = hashlib.md5()
        self.size = os.path.getsize(self.filename) 
        if not self.ignoremtime: self.getmtime()
        self.getheader()
        self.makehash()
        return self.md5.hexdigest()


def parse_args(args):

    parser = argparse.ArgumentParser(description="Run nchash on one or more netCDF files")
    parser.add_argument("-n","--noname", help="Do not include filename in the hash (default False)", action='store_true')
    parser.add_argument("-m","--nomtime", help="Do not include file modification time the hash (default False)", action='store_true')
    parser.add_argument("inputs", help="netCDF files", nargs='+')

    return parser.parse_args(args)

def main(args):

    hashes = defaultdict(list)

    for ncinput in args.inputs:
        try:
            nchash = NCDataHash(ncinput,args.noname,args.nomtime)
            print(nchash.gethash() + "  " + ncinput)
        except NotNetcdfFileError as e:
            sys.stderr.write(str(e))

def main_argv():
    
    args = parse_args(sys.argv[1:])

    main(args)

if __name__ == "__main__":

    main_argv()

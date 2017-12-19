#!/usr/bin/env python

from __future__ import print_function

import hashlib
import netCDF4 as nc
import os, sys
import argparse
import re
from subprocess import check_output
from collections import defaultdict

class NCDataHash(object):
    """A hash used to uniquely identify a netCDF data file
    """

    def __init__(self, filename, noname=False, nomtime=False):
        """Return a DataHash object for filename"""
        self.stripfilename = noname
        self.ignoremtime = nomtime
        self.filename = filename
        self.md5 = hashlib.md5()
        self.size = os.path.getsize(self.filename) 
        if not self.ignoremtime: self.getmtime()
        self.getheader()
        self.makehash()

    def getmtime(self):

        # Tried using h5py to access internal mtime attribute, but
        # this is not always used, so just use modification time

        self.mtime = os.path.getmtime(self.filename) 
        return self.mtime

    def getheader(self):
        self.ncdump = check_output(["ncdump","-h",self.filename])
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
        self.md5.update(self.hashstring)

    def gethash(self):
        return self.md5.hexdigest()


def parse_args(args):

    parser = argparse.ArgumentParser(description="Run ncchk on one or more netCDF files")
    parser.add_argument("-n","--noname", help="Do not include filename in the hash (default False)", action='store_true')
    parser.add_argument("-m","--nomtime", help="Do not include file modification time the hash (default False)", action='store_true')
    parser.add_argument("inputs", help="netCDF files", nargs='+')

    return parser.parse_args(args)

def main(args):

    hashes = defaultdict(list)

    for ncinput in args.inputs:
        nchash = NCDataHash(ncinput,args.noname,args.nomtime)
        print(nchash.gethash() + "  " + ncinput)

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])

    main(args)

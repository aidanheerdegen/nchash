#!/usr/bin/env python

"""
Copyright 2015 ARC Centre of Excellence for Climate Systems Science
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

import pytest
from netCDF4 import Dataset
from numpy import array, arange, dtype
from numpy.testing import assert_array_equal, assert_array_almost_equal
import os, time
from utils import make_simple_netcdf_file, remove_ncfiles, touch, tmpdir, make_tmpdir
from glob import glob

from nchash import NCDataHash

verbose = True

ncfiles = ['simple_xy.nc']

tmpdir = 'test/tmpfiles'

def setup_module(module):
    if verbose: print ("setup_module      module:%s" % module.__name__)
    remove_ncfiles(verbose)
    make_tmpdir()
    make_simple_netcdf_file(ncfiles)
 
def teardown_module(module):
    if verbose: print ("teardown_module   module:%s" % module.__name__)
    remove_ncfiles(verbose)

def test_nchash():

    for f in glob(os.path.join(tmpdir,"*.nc")):

        hashtime = NCDataHash(f).gethash()
        hashnotime = NCDataHash(f,nomtime=True).gethash()
        hashnoname = NCDataHash(f,noname=True,nomtime=True).gethash()

        # Hash should not change if file is unchanged
        assert(NCDataHash(f).gethash() == hashtime)

        mtime = os.path.getmtime(f)
        touch(f,(mtime+1,mtime+1))

        # mtime dependent hash should not match
        assert(NCDataHash(f).gethash() != hashtime)

        # mtime independent hashes should match
        assert(NCDataHash(f,nomtime=True).gethash() == hashnotime)

        # mtime independent hash with different name should match hashnoname
        assert(NCDataHash(f+'.notsamename',noname=True,nomtime=True).gethash() == hashnoname)


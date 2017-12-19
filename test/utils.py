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

from netCDF4 import Dataset
import numpy as np
from glob import glob
import os
import shutil

formats = ['NETCDF3_CLASSIC', 'NETCDF3_64BIT_OFFSET', 'NETCDF4_CLASSIC']

tmpdir = 'test/tmpfiles'

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def make_tmpdir(verbose=True):
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)

def remove_ncfiles(verbose=True):
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)

def touch(fname, times=None):
    # http://stackoverflow.com/a/1160227/4727812
    with open(fname, 'a'):
        os.utime(fname, times)

def make_simple_netcdf_file(ncfiles):

    # the output array to write will be nx x ny
    ny = 600; nx = 120

    # create the output data.
    data = np.reshape(np.arange(nx*ny)/100., (nx,ny))

    for i,form in enumerate(formats):

        filename = ncfiles[0].replace('.nc', "_{}.nc".format(i))
        make_file(filename, form, data)

        filename = ncfiles[0].replace('.nc', "_{}.nc.notsamename".format(i))
        make_file(filename, form, data)

def make_file(filename, form, data):

    filename = os.path.join(tmpdir,filename)
    print("Making {}".format(filename))

    ncfile = Dataset(filename,'w',format=form) 
    nx, ny = data.shape

    # create the x and y dimensions.
    ncfile.createDimension('x',nx)
    ncfile.createDimension('y',ny)

    # create the variable (4 byte integer in this case)
    # first argument is name of variable, second is datatype, third is
    # a tuple with the names of dimensions.
    ncdata = ncfile.createVariable('data',np.dtype('float32').char,('y','x'))
    ncdata.setncattr("Unhidden","test")
    ncdata[:] = data
    ncfile.close()

if __name__ == "__main__":

    make_simple_netcdf_file(['simple_xy.nc'])

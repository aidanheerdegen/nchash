from netCDF4 import Dataset
import numpy as np
from glob import glob
import os
import string
import shutil

formats = ['NETCDF3_CLASSIC', 'NETCDF3_64BIT_OFFSET', 'NETCDF3_64BIT_DATA', 'NETCDF4_CLASSIC']

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

        filename = string.replace(ncfiles[0], '.nc', "_{}.nc".format(i))
        make_file(filename, form, data)

        filename = string.replace(ncfiles[0], '.nc', "_{}.nc.notsamename".format(i))
        make_file(filename, form, data)

def make_file(filename, form, data):

    # print("Making {}".format(filename))
    ncfile = Dataset(os.path.join(tmpdir,filename),'w',format=form) 
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

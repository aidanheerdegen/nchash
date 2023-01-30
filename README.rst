=============================
nchash
=============================

A fast checksum function for netCDF files

.. image:: https://travis-ci.org/aidanheerdegen/nchash.svg?branch=master
  :target: https://travis-ci.org/aidanheerdegen/nchash
.. image:: https://circleci.com/gh/aidanheerdegen/nchash.svg?style=shield
  :target: https://circleci.com/gh/aidanheerdegen/nchash
.. image:: http://codecov.io/github/aidanheerdegen/nchash/coverage.svg?branch=master
  :target: http://codecov.io/github/aidanheerdegen/nchash?branch=master
.. image:: https://landscape.io/github/aidanheerdegen/nchash/master/landscape.svg?style=flat
  :target: https://landscape.io/github/aidanheerdegen/nchash/master
.. image:: https://codeclimate.com/github/aidanheerdegen/nchash/badges/gpa.svg
  :target: https://codeclimate.com/github/aidanheerdegen/nchash
.. image:: https://badge.fury.io/py/nchash.svg
  :target: https://pypi.python.org/pypi/nchash

.. content-marker-for-sphinx

A fast hashing function for netCDF files.

True hashing or checksum functions take longer the larger the file size, and hence don't scale
well for very large files.

The intention of this code was to create something that would be able to detect changes
in files as a "first pass" in a hierarchy of checksums. Full md5 or sha style checksums would 
still be required to robustly identify files.

The specific use case is verifying input files in ocean simulation codes, which are run, checkpointed
and then re-run in a continuous cycle. This allows for a quick integrity check on resubmission, which 
if failed can trigger a slower but more rigorous full checksum comparison.

The code hashes a dump of the netCDF header, the size and the modification time of the file
(internal hdf5 modification time in the case of netCDF4 formatted files).

This hash is unlikely to be robust over long time periods, as there may well be changes to the 
way ncdump outputs the header. But in the use-case envisaged this would trigger a more exhaustive
check, which if successful, could then regenerate a new nchash for fast checking.

Over short to medium timescales, and certainly within the time taken to re-run the simulation this
would be robust to changes. Particularly so for netCDF4 files which have an internal hdf5 modfication
time stamp. In addition, netCDF4 files that are compressed will likely change size with even small
changes to variables in the file.

Testing on an HPC system with fast disk access hashing is independent of size and takes 0.5-0.8s. Testing
has included file sizes up to 100GB.

-------
Install
-------

Conda install::

    conda install -c coecms nchash

Pip install (into a virtual environment)::

    pip install nchash
    
Note, nchash uses the ncdump tool. This is installed automatically when installing nchash with conda, but not when installing with pip.

---
Use
---

-------
Develop
-------

Development install::

    git checkout https://github.com/aidanheerdegen/nchash
    cd nchash
    conda env create -f conda/dev-environment.yml
    source activate nchash-dev
    pip install -e '.[dev]'

The `dev-environment.yml` file is for speeding up installs and installing
packages unavailable on pypi, `requirements.txt` is the source of truth for
dependencies.

Run tests::

    py.test


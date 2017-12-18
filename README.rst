=============================
nchash
=============================

A fast checksum function for netCDF files

.. image:: https://readthedocs.org/projects/nchash/badge/?version=latest
  :target: https://readthedocs.org/projects/nchash/?badge=latest
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

-------
Install
-------

Conda install::

    conda install -c aidanheerdegen nchash

Pip install (into a virtual environment)::

    pip install nchash

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

Build documentation::

    python setup.py build_sphinx
    firefox docs/_build/index.html

Upload documentation::

    git subtree push --prefix docs/_build/html/ origin gh-pages

# MUJIN Controller Python Client Library

![Build status](https://github.com/mujin/mujincontrollerclientpy/actions/workflows/python.yml/badge.svg)

This is an open-source client library communicating with the MUJIN Controller WebAPI.


## Releases and Versioning

- The latest stable build is managed by the **latest_stable** branch, please use it.  It is tested on Linux with python 2.6.5.
  
  - **Do not use master branch** if you are not a developer. 
  
- Versions have three numbers: MAJOR.MINOR.PATCH
  
  - Official releases always have the MINOR and PATCH version as an even number. For example 0.2.4, 0.2.6, 0.4.0, 0.4.2.
  - All versions with the same MAJOR.MINOR number have the same API ande are ABI compatible.
  
- There are `git tags <https://github.com/mujin/mujincontrollerclientpy/tags>`_ for official release like v0.2.4.


## Running on Linux

Load mujincontrollerclient as a module in python.


## Install on Linux

.. code-block:: bash

  BUILD_DIR= # where you want the build files to be, e.g. /path/to/build/
  INSTALL_DIR= # where you want the library to be installed, e.g. /path/to/install/
  python setup.py build --build-base=$BUILD_DIR install --prefix=$INSTALL_DIR --record $BUILD_DIR/installedfiles.txt

  # make sure INSTALL_DIR is on PYTHONPATH
  python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1,prefix='$INSTALL_DIR')" | xargs -I {} python -c "import sys; print 'Is {} on PYTHONPATH?',sys.path.count('{}')>0"


## Uninstall on Linux

.. code-block:: bash

  cat $BUILD_DIR/installedfiles.txt | xargs rm -rf


## Licenses

MUJIN Controller Python Client is Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

In other words, **commercial use and any modifications are allowed**.

Since OpenSSL is included, have to insert the following statement in commercial products::

  This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)


## For Maintainers

TODO

To setup building documentation, checkout `this tutorial <https://gist.github.com/825950>`_ so setup **gh-pages** folder. Then run::

  cd gh-pages
  git pull origin gh-pages
  git rm -rf en ja
  cd ../docs
  rm doxygenhtml_installed_*
  make gh-pages
  cd ../gh-pages
  git commit -m "updated documentation" -a
  git push origin gh-pages

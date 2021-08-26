# MUJIN Controller Python Client Library

![Build status](https://github.com/mujin/mujincontrollerclientpy/actions/workflows/python.yml/badge.svg)

This is an open-source client library communicating with the MUJIN Controller WebAPI.


## Releases and Versioning

- The latest stable build is managed by the **master** branch, please use it. It is tested on Linux with python 3.9.

- Versions have three numbers: MAJOR.MINOR.PATCH
  
  - Official releases always have the MINOR and PATCH version as an even number. For example 0.2.4, 0.2.6, 0.4.0, 0.4.2.
  - All versions with the same MAJOR.MINOR number have the same API ande are ABI compatible.
  
- There are [git tags](https://github.com/mujin/mujincontrollerclientpy/tags) for official release like v0.2.4.


## Running on Linux

Load mujincontrollerclient as a module in python.


## Install on Linux

```bash
pip install .
```

## Licenses

MUJIN Controller Python Client is Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

In other words, **commercial use and any modifications are allowed**.

Since OpenSSL is included, have to insert the following statement in commercial products::

  This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)


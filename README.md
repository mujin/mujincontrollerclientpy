# Mujin Controller Python Client Library

![Build status](https://github.com/mujin/mujincontrollerclientpy/actions/workflows/python.yml/badge.svg)

This is an open-source client library communicating with the Mujin Controller WebAPI.


## Releases and Versioning

- The latest stable build is managed by the **master** branch, please use it. It is tested on Linux with Python 3.9.

- Versions have three numbers: MAJOR.MINOR.PATCH
  
  - All versions with the same MAJOR.MINOR number have the same API ande are ABI compatible.


## Running on Linux

Load mujincontrollerclient as a module in Python.


## Install on Linux

```bash
pip install .
```

## Licenses

Mujin Controller Python Client is Licensed under the Apache License, Version 2.0 (the "License"). See [LICENSE](LICENSE)

## For developers

### How to re-generate `controllergraphclient.py`

First, set up a virtualenv to install required pip packages:

```bash
# create a new virtualenv, you can also delete it afterwards
virtualenv .ve

# install required packages
./.ve/bin/pip install six==1.16.0 requests==2.27.1 pyzmq==22.3.0 graphql-core==3.2.0 typing_extensions==4.2.0

# install mujincontrollerclient
./.ve/bin/pip install .
```

Then, use the `mujin_controllerclientpy_generategraphclient.py` to generate the content of the `controllergraphclient.py` file.

```bash
./.ve/bin/python devbin/mujin_controllerclientpy_generategraphclient.py --url http://controller123 > python/mujincontrollerclient/controllergraphclient.py
````

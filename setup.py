# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 MUJIN Inc
from distutils.core import setup
try:
    from mujincommon.setuptools import Distribution
except ImportError:
    from distutils.dist import Distribution

setup(
    distclass=Distribution,
    name='MujinControllerClient',
    version='0.0.1',
    packages=['mujincontrollerclient',],
    package_dir={'mujincontrollerclient':'python/mujincontrollerclient'},
    locale_dir='locale',
    license='Apache License, Version 2.0',
    long_description=open('README.rst').read(),
)

# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 MUJIN Inc
from distutils.core import setup
try:
    from mujincommon.setuptools import Distribution
except (ImportError, SyntaxError):
    from distutils.dist import Distribution

version = {}
exec(open('python/mujincontrollerclient/version.py').read(), version)

setup(
    distclass=Distribution,
    name='mujincontrollerclient',
    version=version['__version__'],
    packages=['mujincontrollerclient'],
    package_dir={'mujincontrollerclient': 'python/mujincontrollerclient'},
    data_files=[
        # using scripts= will cause the first line of the script being modified for python2 or python3
        # put the scripts in data_files will copy them as-is
        ('bin', ['bin/mujin_controllerclientpy_registerscene.py', 'bin/mujin_controllerclientpy_applyconfig.py', 'bin/mujin_controllerclientpy_runshell.py']),
    ],
    locale_dir='locale',
    license='Apache License, Version 2.0',
    long_description=open('README.md').read(),
    # flake8 compliance configuration
    enable_flake8=True,  # Enable checks
    fail_on_flake=True,  # Fail builds when checks fail
    install_requires=[],
)

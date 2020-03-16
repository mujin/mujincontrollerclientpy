#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import six
import copy
import json
import argparse
import tempfile
import subprocess
import tarfile
import io
import cStringIO
from mujincontrollerclient.controllerclientbase import ControllerClient

try:
    from mujincommon import EnsureDirectory
except ImportError:
    def EnsureDirectory(directory, **kwargs):
        try:
            os.makedirs(directory, **kwargs)
        except OSError:
            # e.errno might not be errno.EEXIST, so it is better to check the directory existence.
            if not os.path.isdir(directory):
                raise

try:
    from mujincommon import ConfigureRootLogger
except ImportError:
    def ConfigureRootLogger(level):
        logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] [%(filename)s:%(lineno)s %(funcName)s] %(message)s', level=level)

import logging
log = logging.getLogger(__name__)


def _PrettifyConfig(config):
    return json.dumps(config, ensure_ascii=False, indent=2, separators=(',', ': '), sort_keys=True) + '\n'


def _DiffConfig(filename, oldconfig, newconfig):
    with tempfile.NamedTemporaryFile(prefix='old-', suffix='-%s' % filename.replace('/', '-'), bufsize=0) as oldfile:
        with tempfile.NamedTemporaryFile(prefix='new-', suffix='-%s' % filename.replace('/', '-'), bufsize=0) as newfile:
            oldfile.write(_PrettifyConfig(oldconfig))
            newfile.write(_PrettifyConfig(newconfig))
            try:
                subprocess.check_call(['diff', '--color', '--unified=5', oldfile.name, newfile.name])
                return False
            except subprocess.CalledProcessError:
                return True


def _ApplyTemplate(config, template, preservedpaths=None):
    newconfig = copy.deepcopy(template)
    
    # preserve the following path in the original config
    if preservedpaths is None:
        # add some basics
        preservedpaths = [
            # ui specific
            'useFallbackUI',
            'usermodepassword',
            'users',
            'cameraHome',
            'tweakstepsize',
            'sourceContainerInfo',
            'sourcecontainername',
            'sourcecontainernames',
            'destContainerInfo',
            'destcontainername',
            'destcontainernames',
            
            # temp settings
            'robotname',
            'robotspeed',
            'robotaccelmult',
            'robotlockmode',
            
            # controller specific
            'sceneuri',
            'robots', # TODO for now skipping this
            'devices', # TODO for now skipping this
            'calibrationParameters', # TODO for now skipping this
        ]
    
    # always preserve network settings!
    preservedpaths += [
        # network specific
        'networkInterfaceSettings',
        'ntpServer',
        'ntpStratum',
    ]
    
    # others


    for path in set(preservedpaths):
        parts = path.split('.')
        parts, key = parts[:-1], parts[-1]

        # navigate to the part of the conf for preservation
        cursor = config
        newcursor = newconfig
        skip = False
        for part in parts:
            if part not in cursor or part not in newcursor:
                skip = True
                break
            if not isinstance(cursor[part], dict):
                log.warn('path is invalid in the current config: %s', path)
                skip = True
                break
            if not isinstance(newcursor[part], dict):
                log.warn('path is invalid in the template config: %s', path)
                skip = True
                break
            cursor = cursor[part]
            newcursor = newcursor[part]
        if skip:
            continue

        # copy the original conf back at that location
        if key in cursor:
            newcursor[key] = copy.deepcopy(cursor[key])

    return newconfig

def _IsEnsensoConfigFilename(filename):
    parts = filename.split('.')
    return len(parts) == 2 and parts[0].isdigit() and parts[1] == 'json'


def _IsSystemConfigFilename(filename):
    return filename in ('controllersystem.conf', 'binpickingsystem.conf', 'teachworkersystem.conf')


def _LoadConfigTar(tar):
    config = {}
    for member in tar.getmembers():
        if not member.isfile():
            continue
        if not member.path.startswith('config/'):
            continue
        filename = member.path[len('config/'):]
        if filename.startswith('ensenso/'):
            if not _IsEnsensoConfigFilename(filename[len('ensenso/'):]):
                continue
        elif not _IsSystemConfigFilename(filename):
            continue
        config[filename] = json.load(tar.extractfile(member))
    return config


def _SaveConfigTar(tar, config):
    for filename, content in config.items():
        content = _PrettifyConfig(content)
        info = tarfile.TarInfo('config/%s' % filename)
        info.size = len(content)
        tar.addfile(info, cStringIO.StringIO(content))


def _LoadConfigDirectory(directory):
    config = {}
    for filename in os.listdir(directory):
        fullfilename = os.path.join(directory, filename)
        if not os.path.isfile(fullfilename):
            continue
        if not _IsSystemConfigFilename(filename):
            continue
        with open(fullfilename, 'r') as f:
            config[filename] = json.load(f)

    if not os.path.isdir(os.path.join(directory, 'ensenso')):
        return config

    for filename in os.listdir(os.path.join(directory, 'ensenso')):
        fullfilename = os.path.join(directory, 'ensenso', filename)
        if not os.path.isfile(fullfilename):
            continue
        if not _IsEnsensoConfigFilename(filename):
            continue
        with open(fullfilename, 'r') as f:
            config['ensenso/%s' % filename] = json.load(f)

    return config


def _SaveConfigDirectory(directory, config):
    for filename, content in config.items():
        content = _PrettifyConfig(content)
        fullfilename = os.path.join(directory, filename)
        EnsureDirectory(os.path.dirname(fullfilename))
        with open(fullfilename, 'w') as f:
            f.write(content)


def _RunMain():
    parser = argparse.ArgumentParser(description='Apply configuration on controller from template')
    parser.add_argument('--loglevel', action='store', type=str, dest='loglevel', default=None, help='the python log level, e.g. DEBUG, VERBOSE, ERROR, INFO, WARNING, CRITICAL [default=%(default)s]')
    parser.add_argument('--schema', action='store', type=str, dest='schema', required=True, help='path to directory containing schemas [default=%(default)s]')
    parser.add_argument('--template', action='store', type=str, dest='template', required=True, help='path to template config directory [default=%(default)s]')
    parser.add_argument('--config', action='store', type=str, dest='config', default=None, help='path to controller config directory, if --controller is not used [default=%(default)s]')
    parser.add_argument('--controller', action='store', type=str, dest='controller', default=None, help='controller ip or hostname, e.g controller123 [default=%(default)s]')
    parser.add_argument('--username', action='store', type=str, dest='username', default='mujin', help='controller username [default=%(default)s]')
    parser.add_argument('--password', action='store', type=str, dest='password', default='mujin', help='controller password [default=%(default)s]')
    parser.add_argument('--force', action='store_true', dest='force', help='apply without confirmation [default=%(default)s]')
    
    options = parser.parse_args()

    # configure logging
    ConfigureRootLogger(level=options.loglevel)

    # check argument
    if options.controller and options.config:
        log.error('need to supply only one of --controller or --config to continue')
        return
    if not options.controller and not options.config:
        log.error('need to supply either --controller or --config to continue')
        return

    # load template
    template = _LoadConfigDirectory(options.template)

    # TODO: load schema
    schema = {}

    # construct client
    if options.controller:
        target = options.controller

        # create client to remote controller
        client = ControllerClient('http://%s' % options.controller, options.username, options.password)
        client.Ping()

        # download config backup from controller
        response = client.Backup(media=False, config=True)
        with tarfile.open(fileobj=io.BytesIO(response.content), mode='r:*') as tar:
            config = _LoadConfigDirectory(tar)
        
    elif options.config:
        target = options.config
        config = _LoadConfigDirectory(options.config)

    # TODO: apply template
    # newconfig = _ApplyTemplate(config, template)
    newconfig = copy.deepcopy(config)

    # debug
    from IPython.terminal import embed
    ipshell = embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals())

    # find what is changed
    changedconfig = {}
    for filename, newcontent in newconfig.items():
        if _DiffConfig(filename, config.get(filename), newcontent):
            changedconfig[filename] = newcontent

    # if the config is different, prompt the user
    if len(changedconfig) == 0:
        log.debug('configuration already up-to-date on %s', target)
        return

    try:
        log.warn('configuration will be changed on %s', target)
        if not options.force:
            six.moves.input('Are you sure about applying the above changes to %s? Press ENTER to continue ...' % target)
    except KeyboardInterrupt:
        print('')
        log.warn('canceled by user')
        return

    # apply the configuration changes
    log.debug('applying configuration on %s', target)
    if options.controller:
        # restore configurations
        output = cStringIO.StringIO()
        with tarfile.open(fileobj=output, mode='w|gz') as tar:
            _SaveConfigTar(tar, changedconfig)
        output.seek(0)
        client.RestoreBackup(output, media=False, config=True)
    elif options.config:
        # write out the entire directory
        _SaveConfigDirectory(options.config, changedconfig)
    log.debug('done')


if __name__ == '__main__':
    _RunMain()

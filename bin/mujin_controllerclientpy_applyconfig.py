#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import logging
log = logging.getLogger(__name__)


def _PrettifyConfig(config):
    return json.dumps(config, ensure_ascii=False, indent=2, separators=(',', ': '), sort_keys=True) + '\n'


def _DiffConfig(oldconfig, newconfig):
    with tempfile.NamedTemporaryFile(prefix='old-config-', suffix='.json', bufsize=0) as oldfile:
        with tempfile.NamedTemporaryFile(prefix='new-config-', suffix='.json', bufsize=0) as newfile:
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


def _RunMain():
    parser = argparse.ArgumentParser(description='Apply configuration on controller from template')
    parser.add_argument('--loglevel', action='store', type=str, dest='loglevel', default=None, help='the python log level, e.g. DEBUG, VERBOSE, ERROR, INFO, WARNING, CRITICAL [default=%(default)s]')
    parser.add_argument('--template', action='store', type=str, dest='template', required=True, help='path to template config directory [default=%(default)s]')
    parser.add_argument('--config', action='store', type=str, dest='config', default=None, help='path to controller config directory, if --controller is not used [default=%(default)s]')
    parser.add_argument('--controller', action='store', type=str, dest='controller', default=None, help='controller ip or hostname, e.g controller123 [default=%(default)s]')
    parser.add_argument('--username', action='store', type=str, dest='username', default='mujin', help='controller username [default=%(default)s]')
    parser.add_argument('--password', action='store', type=str, dest='password', default='mujin', help='controller password [default=%(default)s]')
    parser.add_argument('--force', action='store_true', dest='force', help='apply without confirmation [default=%(default)s]')
    parser.add_argument('--schema', action='append', type=str, dest='schemas', help='additional schemas [default=%(default)s]')
    options = parser.parse_args()

    # configure logging
    try:
        from mujincommon import ConfigureRootLogger
        ConfigureRootLogger(level=options.loglevel)
    except ImportError:
        logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] [%(filename)s:%(lineno)s %(funcName)s] %(message)s', level=options.loglevel)

    # load template
    # TODO: read entire directory
    template = {}
    config = {}

    # construct client
    if options.controller:
        target = options.controller
        client = ControllerClient('http://%s' % options.controller, options.username, options.password)
        client.Ping()

        # download config backup from controller
        response = client.Backup(media=False, config=True)
        with tarfile.open(fileobj=io.BytesIO(response.content), mode='r:*') as tar:
            for member in tar.getmembers():
                if not member.isfile():
                    continue
                if member.path.startswith('config/ensenso/'):
                    filename = member.path[len('config/ensenso/'):]
                    parts = filename.split('.')
                    if len(parts) != 2 or not parts[0].isdigit() or parts[1] != 'json':
                        continue
                    config['ensenso/%s' % filename] = json.load(tar.extractfile(member))

                elif member.path.startswith('config/'):
                    filename = member.path[len('config/'):]
                    if filename not in ('controllersystem.conf', 'binpickingsystem.conf', 'teachworkersystem.conf'):
                        continue

                    config[filename] = json.load(tar.extractfile(member))
        
    elif options.config:
        target = options.config

        # TODO: read the entire directory
        
    else:
        log.error('need to supply either --controller or --config to continue')
        return

    from IPython.terminal import embed
    ipshell = embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals())

    # TODO: apply template
    # newconfig = _ApplyTemplate(config, template)
    newconfig = config

    # if the config is different, prompt the user
    if not _DiffConfig(config, newconfig):
        log.debug('configuration already up-to-date on %s', target)
        # return

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
            for filename, content in newconfig.items():
                content = _PrettifyConfig(content)
                info = tarfile.TarInfo('config/%s' % filename)
                info.size = len(content)
                tar.addfile(info, cStringIO.StringIO(content))
        output.seek(0)
        client.RestoreBackup(output, media=False, config=True)
    elif options.config:
        # TODO: write out the entire directory
        pass
    log.debug('done')


if __name__ == '__main__':
    _RunMain()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import copy
import json
import argparse
import tempfile
import subprocess
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


def _ApplyTemplate(config, template):
    newconfig = copy.deepcopy(template)

    # preserve the following path in the original config
    preservedpaths = (
        'cameraHome',

        'networkInterfaceSettings',
        'ntpServer',
        'ntpStratum',

        'useFallbackUI',
        'motionUI',

        'tweakstepsize',

        'robotspeed',
        'robotaccelmult',

        'robots', # TODO for now skipping this
        'devices', # TODO for now skipping this
        'calibrationParameters', # TODO for now skipping this

        'sourceContainerInfo',
        'sourcecontainername',
        'sourcecontainernames',
        'destContainerInfo',
        'destcontainername',
        'destcontainernames',

        'binpickingparameters.predictDetectionInfo.alignLongAxisToX',
        'binpickingparameters.predictDetectionInfo.alignLongAxisToY',
        'binpickingparameters.labelerDirection',

        'sceneuri',
    )

    for path in preservedpaths:
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
    parser.add_argument('--template', action='store', type=str, dest='template', default=None, help='path to template config file [default=%(default)s]')
    parser.add_argument('--controller', action='store', type=str, dest='controller', default=None, help='controller ip or hostname, e.g controller123 [default=%(default)s]')
    parser.add_argument('--config', action='store', type=str, dest='config', default=None, help='controller ip or hostname, e.g binpickingsystem.conf [default=%(default)s]')
    parser.add_argument('--username', action='store', type=str, dest='username', default='mujin', help='controller username [default=%(default)s]')
    parser.add_argument('--password', action='store', type=str, dest='password', default='mujin', help='controller password [default=%(default)s]')
    parser.add_argument('--force', action='store_true', dest='force', help='apply without confirmation [default=%(default)s]')
    options = parser.parse_args()

    # configure logging
    try:
        from mujincommon import ConfigureRootLogger
        ConfigureRootLogger(level=options.loglevel)
    except ImportError:
        logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] [%(filename)s:%(lineno)s %(funcName)s] %(message)s', level=options.loglevel)

    # load template
    with open(options.template, 'r') as f:
        template = json.load(f)

    # construct client
    if options.controller:
        client = ControllerClient('http://%s' % options.controller, options.username, options.password)
        client.Ping()
        config = client.GetConfig()
        target = client.controllerIp
    elif options.config:
        with open(options.config, 'r') as f:
            config = json.load(f)
        target = options.config
    else:
        log.error('need to supply either --controller or --config to continue')
        return

    # apply template
    newconfig = _ApplyTemplate(config, template)

    # if the config is different, prompt the user
    if not _DiffConfig(config, newconfig):
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
        client.SetConfig(newconfig)
    elif options.config:
        with open(options.config, 'w') as f:
            f.write(_PrettifyConfig(newconfig))
    log.debug('done')


if __name__ == '__main__':
    _RunMain()

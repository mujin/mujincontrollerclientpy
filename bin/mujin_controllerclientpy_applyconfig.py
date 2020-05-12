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


def _MergeDicts(x, y):  # for python 2 compatibility
    z = copy.deepcopy(x)
    z.update(y)
    return z


def _ShowDiffInOneLine(oldconfig, newconfig, parentPath=None, useColours=True):
    colourCodes = {'cc_restore': '\033[00m', 'cc_mod': '\033[01;34m', 'cc_add': '\033[01;32m', 'cc_del': '\033[01;31m'}
    colourCodesDummy = zip([(key, '') for key in colourCodes.keys()])

    if not (isinstance(newconfig, dict) and isinstance(oldconfig, dict)) and not (isinstance(newconfig, list) and isinstance(oldconfig, list)):
        log.warn('Type of config needs to be either of dict or list.')
        return

    if isinstance(newconfig, list) and len(newconfig) != len(oldconfig):
        absolutePathStr = '.'.join(parentPath or [])
        print('[%(cc_mod)sMOD%(cc_restore)s] %(cc_mod)s%(path)s%(cc_restore)s=%(cc_add)s%(newvalue)s%(cc_restore)s (old: %(cc_del)s%(oldvalue)s%(cc_restore)s) [size changed to %(newsize)d from %(oldsize)d]' % _MergeDicts({
            'path': absolutePathStr, 'newvalue': newconfig, 'oldvalue': oldconfig, 'newsize': len(newconfig), 'oldsize': len(oldconfig)
        }, colourCodes if useColours else colourCodesDummy))
        return

    for key in sorted(newconfig) if isinstance(newconfig, dict) else range(len(newconfig)):
        absolutePathStr = '.'.join((parentPath or []) + [key if isinstance(newconfig, dict) else '[%d]'%key])
        if (isinstance(newconfig, dict) and key not in oldconfig):
            print('[%(cc_add)sADD%(cc_restore)s] %(cc_add)s%(path)s%(cc_restore)s=%(cc_add)s%(newvalue)s%(cc_restore)s' % _MergeDicts({
                'path': absolutePathStr, 'newvalue': newconfig[key]
            }, colourCodes if useColours else colourCodesDummy))

        elif type(oldconfig[key]) != type(newconfig[key]): # noqa: E721
            # key exists in both confs, but types don't match
            print('[%(cc_mod)sMOD%(cc_restore)s] %(cc_mod)s%(path)s%(cc_restore)s=%(cc_add)s%(newvalue)s%(cc_restore)s (old: %(cc_del)s%(oldvalue)s%(cc_restore)s) [type changed to %(newtype)s from %(oldtype)s]' % _MergeDicts({
                'path': absolutePathStr, 'newvalue': newconfig[key], 'oldvalue': oldconfig[key], 'newtype': type(newconfig), 'oldtype': type(oldconfig)
            }, colourCodes if useColours else colourCodesDummy))

        else:
            # key exists in both confs with same type values
            if isinstance(newconfig[key], dict) or isinstance(newconfig[key], list):
                _ShowDiffInOneLine(oldconfig[key], newconfig[key], parentPath=(parentPath or [])+[key if isinstance(newconfig, dict) else '[%d]'%key], useColours=useColours)
            elif newconfig[key] != oldconfig[key]:
                print('[%(cc_mod)sMOD%(cc_restore)s] %(cc_mod)s%(path)s%(cc_restore)s=%(cc_add)s%(newvalue)s%(cc_restore)s (old: %(cc_del)s%(oldvalue)s%(cc_restore)s)' % _MergeDicts({
                    'path': absolutePathStr, 'newvalue': newconfig[key], 'oldvalue': oldconfig[key]
                }, colourCodes if useColours else colourCodesDummy))

            else:
                pass  # same value

    if isinstance(newconfig, dict):
        for key in list(set(oldconfig.keys()) - set(newconfig.keys())):
            absolutePathStr = '.'.join((parentPath or []) + [key])
            print('[%(cc_del)sDEL%(cc_restore)s] %(cc_del)s%(path)s%(cc_restore)s (old: %(cc_del)s%(oldvalue)s%(cc_restore)s)' % _MergeDicts({
                'path': absolutePathStr, 'oldvalue': oldconfig[key]
            }, colourCodes if useColours else colourCodesDummy))


def _DiffConfig(oldconfig, newconfig, showInOneLine=False):
    with tempfile.NamedTemporaryFile(prefix='old-config-', suffix='.json', bufsize=0) as oldfile:
        with tempfile.NamedTemporaryFile(prefix='new-config-', suffix='.json', bufsize=0) as newfile:
            oldfile.write(_PrettifyConfig(oldconfig))
            newfile.write(_PrettifyConfig(newconfig))
            if showInOneLine:
                res = None
                try:
                    subprocess.check_call(['cmp', '-s', oldfile.name, newfile.name])
                    res = False
                except subprocess.CalledProcessError:
                    res = True
                if res:
                    _ShowDiffInOneLine(oldconfig, newconfig)
                return res
            else:
                try:
                    subprocess.check_call(['diff', '--color', '--unified=5', oldfile.name, newfile.name])
                    return False
                except subprocess.CalledProcessError:
                    return True


def _CopyValueOfPath(src, dest, path, parentPath=None):
    currentPathElement = path[0]
    if currentPathElement == '*':
        if isinstance(src, dict) and isinstance(dest, dict):
            for srcKey, srcValue in src.iteritems():
                if srcKey in dest:
                    _CopyValueOfPath(srcValue, dest[srcKey], path[1:], (parentPath or [])+[path[0]])
                else:
                    log.warn('Key %s does not exist in destination conf: %s' % (srcKey, '.'.join(parentPath or ['(root)'])))

        elif isinstance(src, list) and isinstance(dest, list):
            for index in range(len(src)):
                if len(dest) > index:
                    _CopyValueOfPath(src[index], dest[index], path[1:], (parentPath or [])+[path[0]])
                else:
                    log.warn('Index %d is out of range in destination conf: %s' % (index, '.'.join(parentPath or ['(root)'])))
                    break

        else:
            log.warn('Wildcard can be applied only on dict or list: %s' % '.'.join(parentPath or ['(root)']))

    else:
        if isinstance(src, dict) and isinstance(dest, dict):
            if currentPathElement not in src:
                return
        elif isinstance(src, list) and isinstance(dest, list):
            currentPathElement = int(currentPathElement)
            if len(src) <= currentPathElement:
                return
            elif len(dest) <= currentPathElement:
                log.warn('Index %d is out of range in destination conf: %s' % (currentPathElement, '.'.join(parentPath or ['(root)'])))
                return
        else:
            log.warn('Element needs to be either of dict or list: %s' % '.'.join(parentPath or ['(root)']))
            return

        if len(path) == 1:
            dest[currentPathElement] = copy.deepcopy(src[currentPathElement])
        else:
            _CopyValueOfPath(src[currentPathElement], dest[currentPathElement], path[1:], (parentPath or [])+[path[0]])


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


    for pathStr in set(preservedpaths):
        path = pathStr.split('.')
        _CopyValueOfPath(config, newconfig, path)

    return newconfig


def _RunMain():
    parser = argparse.ArgumentParser(description='Apply configuration on controller from template')
    parser.add_argument('--loglevel', action='store', type=str, dest='loglevel', default=None, help='the python log level, e.g. DEBUG, VERBOSE, ERROR, INFO, WARNING, CRITICAL [default=%(default)s]')
    parser.add_argument('--template', action='store', type=str, dest='template', required=True, help='path to template config file [default=%(default)s]')
    parser.add_argument('--preserve', action='store', type=str, dest='preserve', default=None, help='path to a file containing the list of additional keys to preserve while merging template [default=%(default)s]')
    parser.add_argument('--controller', action='store', type=str, dest='controller', default=None, help='controller ip or hostname, e.g controller123 [default=%(default)s]')
    parser.add_argument('--username', action='store', type=str, dest='username', default='mujin', help='controller username [default=%(default)s]')
    parser.add_argument('--password', action='store', type=str, dest='password', default='mujin', help='controller password [default=%(default)s]')
    parser.add_argument('--config', action='store', type=str, dest='config', default=None, help='path to input config file. If specified, the config file is loaded as input instead of obtaining from controller [default=%(default)s]')
    parser.add_argument('--force', action='store_true', dest='force', default=False, help='apply without confirmation [default=%(default)s]')
    parser.add_argument('--dryrun', action='store_true', dest='dryrun', default=False, help='shows differences and quit [default=%(default)s]')
    parser.add_argument('--oneline', action='store_true', dest='oneline', default=False, help='shows each difference in one line [default=%(default)s]')
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

    # load preservelist
    preservedpaths = None
    if options.preserve:
        preservedpaths = []
        with open(options.preserve, 'r') as f:
            for line in f.read().strip().split('\n'):
                line = line.split('#')[0].strip()
                if line:
                    preservedpaths.append(line)

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
    newconfig = _ApplyTemplate(config, template, preservedpaths=preservedpaths)

    # if the config is different, prompt the user
    if not _DiffConfig(config, newconfig, showInOneLine=options.oneline):
        log.debug('configuration already up-to-date on %s', target)
        return

    try:
        if options.dryrun:
            return
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

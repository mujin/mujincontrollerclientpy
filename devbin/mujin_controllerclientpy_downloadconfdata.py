#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import logging
log = logging.getLogger(__name__)

def _ConfigureLogging(level=None):
    try:
        import mujincommon
        mujincommon.ConfigureRootLogger(level=level)
    except ImportError:
        logging.basicConfig(format='%(levelname)s %(name)s: %(funcName)s, %(message)s', level=logging.DEBUG)

def _ParseArguments():
    import argparse
    parser = argparse.ArgumentParser(description='Downloads all config files, currently used scene, and currently selected target env file from a controller')
    parser.add_argument('--loglevel', type=str, default=None, help='The python log level, e.g. DEBUG, VERBOSE, ERROR, INFO, WARNING, CRITICAL (default: %(default)s)')
    parser.add_argument('--url', type=str, default='http://127.0.0.1', help='URL of the controller (default: %(default)s)')
    parser.add_argument('--username', type=str, default='mujin', help='Username to login with (default: %(default)s)')
    parser.add_argument('--password', type=str, default='mujin', help='Password to login with (default: %(default)s)')
    return parser.parse_args()

def _GetControllerClient(url, username, password):
    from mujincontrollerclient import controllerclientbase

    # create a controller client for the controller
    log.info('connecting to %s', url) 
    return controllerclientbase.ControllerClient(
        controllerurl=url,
        controllerusername=username,
        controllerpassword=password,
    )

def _GetScenes(controllerClient):
    from mujincontrollerclient import uriutils

    # get the conf file
    config = controllerClient.GetConfig()

    # get the current scene uri from config
    sceneList = []
    sceneExtension = '.msgpack'
    sceneUri = config.get('sceneuri', '')
    if sceneUri != '':
        sceneExtension = os.path.splitext(sceneUri)[-1]
        sceneList.append(uriutils.GetPrimaryKeyFromURI(sceneUri))

    # get target names from config
    for targetname in config.get('selectedtargetnames', []):
        if not targetname.startswith('mujin:'):
            # use current scene's extension
            targetname = 'mujin:/%s.mujin%s'%(targetname, sceneExtension)
        sceneList.append(uriutils.GetPrimaryKeyFromURI(targetname))

    return sceneList

def _DownloadBackup(controllerClient, sceneList):
    import re
    import tarfile

    log.info('downloading scenes %s and all configs', sceneList)
    response = controllerClient.Backup(      
        saveconfig=True,
        backupscenepks=sceneList,
        timeout=600.0,
    )

    # extract the response, use the name supplied by webstack
    archiveFilename = re.findall('filename=(.+)', response.headers['Content-Disposition'])[0].strip('"')
    downloadFoldername = os.path.join(os.getcwd(), archiveFilename.rstrip('.tar.gz'))
    log.info('saving downloaded data to %s', downloadFoldername)
    with tarfile.open(fileobj=response.raw, mode='r|gz') as tar:
        tar.extractall(path=downloadFoldername)

def _Main():
    options = _ParseArguments()
    _ConfigureLogging(options.loglevel)

    controllerClient = _GetControllerClient(options.url, options.username, options.password)
    sceneList = _GetScenes(controllerClient)
    _DownloadBackup(controllerClient, sceneList)

if __name__ == "__main__":
    _Main()
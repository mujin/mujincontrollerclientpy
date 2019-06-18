#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import argparse

from mujincontrollerclient import controllerclientbase, urlparse, json

import logging
log = logging.getLogger(__name__)

logging.basicConfig(format='%(levelname)s %(name)s: %(funcName)s, %(message)s', level=logging.INFO)

if __name__ == "__main__":
    MUJIN_CONFIG_DIR = os.environ.get('MUJIN_CONFIG_DIR', 'conf')
    MUJIN_BINPICKINGUI_CONFIG = os.environ.get('MUJIN_BINPICKINGUI_CONFIG', '') or os.path.join(MUJIN_CONFIG_DIR, 'binpickingsystem.conf')
    parser = argparse.ArgumentParser(description='Registers a scene given the filename and the system conf file from MUJIN_BINPICKINGUI_CONFIG and MUJIN_CONFIG_DIR env variables.')
    parser.add_argument('--config', action='store', type=str, dest='config', default=MUJIN_BINPICKINGUI_CONFIG, help="path to binpicking config file")
    parser.add_argument('--url', action='store', type=str, dest='url', default=None, help="URL to the controller to override the conf file and communicate with another controller. Format is: http://testuser:pass@controller100")
    parser.add_argument('--newname', action='store', type=str, dest='newname', default=None, help="New name to give to the scene filename and to rename the scene")
    parser.add_argument('--overwritename', action='store_true', dest='overwritename', default=False, help="If true, then will use the base name of the filename to overwrite the new name of the scene.")
    (options, args) = parser.parse_known_args()

    if len(args) == 0:
        log.warn(u'need to specify a scene to register')
        sys.exit(1)

    scenefilename = args[0]

    if not os.path.exists(scenefilename):
        raise ValueError('could not find scene %s' % scenefilename)

    if options.url is not None:
        urlobj = urlparse.urlparse(options.url)
        username = 'testuser'
        password = 'pass'
        if urlobj.username is not None:
            username = urlobj.username
        if urlobj.password is not None:
            password = urlobj.password
        self = controllerclientbase.ControllerClient(options.url, username, password)
    else:
        conffile = options.config
        if not os.path.exists(conffile):
            conffile = os.path.join(os.environ['MUJIN_CONFIG_DIR'], 'controllersystem.conf')
            if not os.path.exists(conffile):
                log.warn(u'could not find conf file at %s', os.environ['MUJIN_CONFIG_DIR'])
                sys.exit(2)

        userconf = json.load(open(conffile, 'r'))

        MUJIN_BINPICKINGUI_CONTROLLER_USERNAME = os.environ.get('MUJIN_BINPICKINGUI_CONTROLLER_USERNAME', 'mujin').strip()
        MUJIN_BINPICKINGUI_CONTROLLER_PASSWORD = os.environ.get('MUJIN_BINPICKINGUI_CONTROLLER_PASSWORD', '').strip() or os.environ.get('MUJIN_WEBSTACK_%s_PASSWORD' % MUJIN_BINPICKINGUI_CONTROLLER_USERNAME, '').strip() or ''
        self = controllerclientbase.ControllerClient(userconf.get('controllerurl','') or 'http://localhost', userconf.get('controllerusername','') or MUJIN_BINPICKINGUI_CONTROLLER_USERNAME, userconf.get('controllerpassword','') or MUJIN_BINPICKINGUI_CONTROLLER_PASSWORD)
    
    scenebasename = os.path.split(scenefilename)[1]
    if self.FileExists(scenebasename):
        response = input('File %s exists on server, would you like to overwrite? (y/n) ' % scenebasename)
        if response != 'y':
            sys.exit(0)

    self.UploadFile(open(scenefilename, 'r'), filename=scenebasename)
    scenedata = self.CreateScene({'uri': u'mujin:/' + scenebasename, 'overwrite': True})

    if options.newname is not None:
        self.SetScene(scenedata['pk'], {'name': options.newname})
        scenedata['name'] = options.newname
    elif options.overwritename:
        newname = scenebasename.split('.', 1)[0]
        self.SetScene(scenedata['pk'], {'name': newname})
        scenedata['name'] = newname

    log.info('successfully registered %s with name %s and %d objects', scenebasename, scenedata.get('name', None), len(scenedata.get('instobjects', [])))

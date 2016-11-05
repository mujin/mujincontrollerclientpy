#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
from mujincontrollerclient import controllerclientbase

import logging
log = logging.getLogger(__name__)

logging.basicConfig(format='%(levelname)s %(name)s: %(funcName)s, %(message)s', level=logging.INFO)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        log.info('Registers a scene given the filename and the system conf file from MUJIN_CONFIG_DIR env variable')
        sys.exit(1)
        
    scenefilename = sys.argv[1]
    
    assert(os.path.exists(scenefilename))
    
    conffile = os.path.join(os.environ['MUJIN_CONFIG_DIR'], 'binpickingsystem.conf')
    if not os.path.exists(conffile):
        conffile = os.path.join(os.environ['MUJIN_CONFIG_DIR'], 'controllersystem.conf')
        if not os.path.exists(conffile):
            log.warn(u'could not find conf file at %s', os.environ['MUJIN_CONFIG_DIR'])
            sys.exit(2)
    
    userconf = json.load(open(conffile,'r'))
    
    self = controllerclientbase.ControllerClient(userconf['controllerurl'], userconf['controllerusername'], userconf['controllerpassword'])
    
    scenebasename = os.path.split(scenefilename)[1]
    if self.FileExists(scenebasename):
        response = raw_input(u'File %s exists on server, would you like to overwrite? (y/n) '%scenebasename)
        if response != 'y':
            sys.exit(0)
    
    self.UploadFile(scenebasename, open(scenefilename).read())
    content = self.CreateScene({'uri':u'mujin:/'+scenebasename, 'overwrite':True})
    log.info(u'successfully registered %s with %d objects', scenebasename, len(content.get('instobjects',[])))

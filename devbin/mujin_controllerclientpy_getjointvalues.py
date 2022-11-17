#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import argparse

import mujincontrollerclient
from mujincontrollerclient import controllerwebclientv1, urlparse, json, binpickingcontrollerclient

import logging
log = logging.getLogger(__name__)

logging.basicConfig(format='%(levelname)s %(name)s: %(funcName)s, %(message)s', level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get joint values of the robot and return ipython terminal.')
    parser.add_argument('--url', action='store', type=str, dest='url', default=None, help="URL to the controller to override the conf file and communicate with another controller. Format is: http://testuser:pass@controller100")
    parser.add_argument('--slaverequestid', action='store', type=str, dest='slaverequestid', default=None, help="salve request id to create/connect on Mujin motino controller. For pickworker the slaverequestId template is the following: 'c%(controllernumber)_pw%(index)', so if you have controller100 and want to connect to the pickworker slave 0 then slaverequestId should be 'c100_pw0'. (by default Mujin pendant scene viewer to pickworker slave 0)")
    (options, args) = parser.parse_known_args()
    slaverequestid=options.slaverequestid
    if slaverequestid is None:
        raise BaseException('No slaverequestid defined')

    # parst url
    if options.url is not None:
        urlobj = urlparse.urlparse(options.url)
        username = 'mujin'
        password = 'mujin'
        if urlobj.username is not None:
            username = urlobj.username
        if urlobj.password is not None:
            password = urlobj.password
        self = controllerwebclientv1.ControllerWebClientV1(options.url, username, password)
    else:
        raise BaseException('No uri defined')
    
    userconf = self.GetConfig()
    robotname = userconf.get('robotname', None)
    if robotname is None:
        raise mujincontrollerclient.ControllerClientError('Failed to get robotname from the config!')
    robots = userconf.get('robots', None)
    devices = userconf.get('devices', None)

    sceneuri = userconf['sceneuri']
    scenebasename = os.path.split(sceneuri)[1]

    binpickingclient = binpickingcontrollerclient.BinpickingControllerClient(controllerurl=options.url, controllerusername=username, controllerpassword=password, scenepk=scenebasename, robotname=robotname, envclearance=userconf.get('envclearance', 20.0), robotspeed=userconf.get('robotspeed', 0.1), robotaccelmult=userconf.get('robotaccelmult', 0.01), taskzmqport=7110, taskheartbeatport=None, taskheartbeattimeout=10.0, robotBridgeConnectionInfo=None, slaverequestid=slaverequestid)

    ret = binpickingclient.GetJointValues()
    currentjointvalues = ret['currentjointvalues']
    log.info('currentjointvalues=%r', currentjointvalues)

    from IPython.terminal import embed; ipshell=embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals(), global_ns=globals())

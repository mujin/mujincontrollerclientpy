#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import argparse
import json
import mujincommon
from mujincontrollerclient import uriutils, planningclient


def ConfigurePlanningserver(level, config, taskzmqport=11000):
    controllerurl = config.get('controllerurl', '').strip() or 'http://127.0.0.1'
    routerport = os.environ.get('MUJIN_PLANNINGSERVER_MASTER_ROUTER_PORT', taskzmqport)
    client = planningclient.PlanningControllerClient(
        taskzmqport=routerport,
        taskheartbeatport=None,
        taskheartbeattimeout=None,
        tasktype=None,
        scenepk=uriutils.GetPrimaryKeyFromURI(config.get('sceneuri', '')),
        usewebapi=False,
        controllerurl=controllerurl)
    client.SetLogLevel(level)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set planningserver logging level')
    parser.add_argument('--loglevel', action='store', type=str, dest='logLevel', default=None, help='Set logging level for webstack')
    parser.add_argument('--conf', action='store', type=str, dest='conf', default=None, help='binpicking conf')
    options = parser.parse_args()
    configFilename = options.conf
    if configFilename is None:
        configFilename = mujincommon.GetExistingConfigFilename()
    with open(configFilename, 'r') as f:
        config = json.loads(f.read())
    ConfigurePlanningserver(options.logLevel, config)

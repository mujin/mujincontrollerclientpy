#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mujinplanningclient.realtimerobotplanningclient import RealtimeRobotPlanningClient

import logging
log = logging.getLogger(__name__)


def _ParseArguments():
    import argparse
    parser = argparse.ArgumentParser(description='Open a shell to use controllerclient')
    parser.add_argument('--loglevel', type=str, default=None, help='The python log level, e.g. DEBUG, VERBOSE, ERROR, INFO, WARNING, CRITICAL (default: %(default)s)')
    parser.add_argument('--url', type=str, default='http://localhost', help='URL of the controller (default: %(default)s)')
    parser.add_argument('--username', type=str, default='mujin', help='Username to login with (default: %(default)s)')
    parser.add_argument('--password', type=str, default='mujin', help='Password to login with (default: %(default)s)')
    return parser.parse_args()


def _ConfigureLogging(level=None):
    try:
        import mujincommon
        mujincommon.ConfigureRootLogger(level=level)
    except ImportError:
        logging.basicConfig(format='%(levelname)s %(name)s: %(funcName)s, %(message)s', level=logging.DEBUG)


def _Main():
    options = _ParseArguments()
    _ConfigureLogging(options.loglevel)

    self = RealtimeRobotPlanningClient(controllerurl=options.url, controllerusername=options.username, controllerpassword=options.password)

    from IPython.terminal import embed
    ipshell = embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals())


if __name__ == "__main__":
    _Main()

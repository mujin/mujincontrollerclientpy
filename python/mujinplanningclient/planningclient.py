# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 MUJIN Inc
"""
Client to connect to Mujin Controller's planning server.
"""

# System imports
import os
import time

# Mujin imports
from mujinwebstackclient import APIServerError
from mujinwebstackclient import urlparse
from mujinwebstackclient.webstackclient import GetURIFromPrimaryKey, GetFilenameFromURI

from . import zmqclient
from . import zmqsubscriber
from . import zmq
from . import json

# Logging
import logging
log = logging.getLogger(__name__)

def GetAPIServerErrorFromZMQ(response):
    """If response is an error, return the APIServerError instantiated from the response's error field. Otherwise return None
    """
    if response is None:
        return None
    
    if 'error' in response:
        if isinstance(response['error'], dict):
            return APIServerError(response['error']['description'], response['error']['errorcode'], response['error'].get('inputcommand',None), response['error'].get('detailInfoType',None), response['error'].get('detailInfo',None))
        
        else:
            return APIServerError(response['error'])
    
    elif 'exception' in response:
        return APIServerError(response['exception'])
    
    elif 'status' in response and response['status'] != 'succeeded':
        # something happened so raise exception
        return APIServerError(u'Resulting status is %s' % response['status'])

def ParseControllerInfo(controllerUrl, username, password):
    """Return controller URL, username, password, port and IP/hostname. This is done because the URL can contain the username and password information.
    """
    # Parse controllerUrl
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(controllerUrl)
    controllerusername = ''
    controllerpassword = ''

    # Parse any credential in the url
    if '@' in netloc:
        creds, netloc = netloc.rsplit('@', 1)
        controllerusername, controllerpassword = creds.split(':', 1)

    # Parse IP (better: hostname) and port
    controllerIp = netloc.split(':', 1)[0]
    if ':' in netloc:
        hostname, port = netloc.split(':')
        controllerIp = hostname

    controllerUrl = urlparse.urlunparse((scheme, netloc, '', '', '', ''))
    controllerusername = controllerusername or username
    controllerpassword = controllerpassword or password
    return controllerUrl, controllerusername, controllerpassword, controllerIp

class PlanningClient(object):
    """Mujin controller client for planning tasks
    """
    _userinfo = None  # A dict storing user info, like locale

    controllerurl = ''  # Mujin Controller URL
    controllerusername = ''  # Username to login to the Mujin Controller
    controllerpassword = ''  # Password to login to the Mujin Controller

    controllerIp = ''  # Hostname of the Mujin Controller

    _sceneparams = None
    scenepk = None  # The scenepk this controller is configured for
    _ctx = None  # zmq context shared among all clients
    _ctxown = None  # zmq context owned by this class
    _commandsocket = None  # zmq client to the command port
    _configsocket = None  # zmq client to the config port
    taskheartbeatport = None  # Port of the task's zmq server's heartbeat publisher, e.g. 7111
    taskheartbeattimeout = None  # Seconds until reinitializing task's zmq server if no heartbeat is received, e.g. 7

    _subscriber = None # an instance of ZmqSubscriber
    _callerid = None # caller identification string to be sent with every command

    def __init__(
        self,
        taskzmqport=11000,
        taskheartbeatport=11001,
        taskheartbeattimeout=7.0,
        tasktype="realtimerobottask3",
        scenepk="",
        ctx=None,
        slaverequestid=None,
        controllerip='',
        controllerurl='http://127.0.0.1',
        controllerusername='',
        controllerpassword='',
        callerid=None,
        **ignoredArgs  # Other keyword args are not used, but extra arguments is allowed for easy initialization from a dictionary
    ):
        """Logs into the Mujin controller and initializes the connection to the planning server (using ZMQ).

        Args:
            taskzmqport (int, optional): Port of the task's ZMQ server
            taskheartbeatport (int, optional): Port of the task's ZMQ server's heartbeat publisher
            taskheartbeattimeout (float, optional): Seconds until reinitializing task's ZMQ server if no heartbeat is received, e.g. 7
            tasktype (str, optional): Type of the task, e.g. 'binpicking', 'handeyecalibration', 'itlrealtimeplanning3'
            scenepk (str, optional): Primary key (pk) of the scene, e.g. irex_demo.mujin.dae
            controllerip (str, optional): Ip or hostname of the mujin controller, e.g. controller14 or 172.17.0.2
            controllerurl (str, optional): (Deprecated; use controllerip instead) URL of the mujin controller, e.g. http://controller14.
            controllerusername (str, optional): Username for the Mujin controller, e.g. testuser
            controllerpassword (str, optional): Password for the Mujin controller
            callerid (str, optional): Caller identifier to send to server on every command
        """
        self._slaverequestid = slaverequestid
        self._sceneparams = {}

        # Task
        self.tasktype = tasktype

        if controllerip:
            self.controllerIp = controllerip
            self.controllerusername = controllerusername
            self.controllerpassword = controllerpassword
        else:
            self.controllerurl, self.controllerusername, self.controllerpassword, self.controllerIp = ParseControllerInfo(controllerurl, controllerusername, controllerpassword)

        self._userinfo = {
            'username': self.controllerusername,
            'locale': os.environ.get('LANG', ''),
        }

        # Connects to task's zmq server
        self._commandsocket = None
        self._configsocket = None
        if taskzmqport is not None:
            if ctx is None:
                self._ctx = zmq.Context()
                self._ctxown = self._ctx
            else:
                self._ctx = ctx
            self.taskzmqport = taskzmqport
            self._commandsocket = zmqclient.ZmqClient(self.controllerIp, taskzmqport, ctx)
            self._configsocket = zmqclient.ZmqClient(self.controllerIp, taskzmqport + 2, ctx)

            self.taskheartbeatport = taskheartbeatport
            self.taskheartbeattimeout = taskheartbeattimeout

        self.SetScenePrimaryKey(scenepk)

        self._callerid = callerid

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()
        if self._subscriber is not None:
            self._subscriber.Destroy()
            self._subscriber = None
        if self._commandsocket is not None:
            self._commandsocket.Destroy()
            self._commandsocket = None
        if self._configsocket is not None:
            self._configsocket.Destroy()
            self._configsocket = None
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
            except Exception:
                pass
            self._ctxown = None

    def SetDestroy(self):
        commandsocket = self._commandsocket
        if commandsocket is not None:
            commandsocket.SetDestroy()
        configsocket = self._configsocket
        if configsocket is not None:
            configsocket.SetDestroy()

    def GetSlaveRequestId(self):
        return self._slaverequestid

    def GetCommandSocketRaw(self):
        return self._commandsocket

    def DeleteJobs(self, timeout=5):
        """Cancels all jobs"""
        if self._configsocket is not None:
            self.SendConfig({'command': 'cancel'}, timeout=timeout, fireandforget=False)

    def GetPublishedServerState(self, timeout=2.0):
        """Return most recent published state. If publishing is disabled, then will return None
        """
        if self._subscriber is None:
            self._subscriber = zmqsubscriber.ZmqSubscriber('tcp://%s:%d' % (self.controllerIp, self.taskheartbeatport or (self.taskzmqport + 1)), ctx=self._ctx)
        rawServerState = self._subscriber.SpinOnce(timeout=timeout)
        if rawServerState is not None:
            return json.loads(rawServerState)
        return None

    def GetPublishedTaskState(self, timeout=2.0):
        """Return most recent published state. If publishing is disabled, then will return None
        """
        serverState = self.GetPublishedServerState(timeout=timeout)
        if serverState is not None and 'slavestates' in serverState:
            return serverState['slavestates'].get('slaverequestid-%s' % self._slaverequestid)
        return None
    
    def SetScenePrimaryKey(self, scenepk):
        self.scenepk = scenepk
        sceneuri = GetURIFromPrimaryKey(scenepk)
        # for now (HACK) need to set the correct scenefilename. newer version of mujin controller need only scenepk, so remove scenefilename eventually
        mujinpath = os.path.join(os.environ.get('MUJIN_MEDIA_ROOT_DIR', '/var/www/media/u'), self.controllerusername)
        scenefilename = GetFilenameFromURI(sceneuri, mujinpath)[1]
        self._sceneparams = {'scenetype': 'mujin', 'sceneuri': sceneuri, 'scenefilename': scenefilename, 'scale': [1.0, 1.0, 1.0]}  # TODO: set scenetype according to the scene
    
    #
    # Tasks related
    #

    def ExecuteCommand(self, taskparameters, slaverequestid=None, timeout=None, fireandforget=None, respawnopts=None, checkpreempt=True, forcereload=False):
        """Executes command with taskparameters via ZMQ.

        Args:
            taskparameters (dict): Task parameters in json format
            timeout (float): Timeout in seconds
            fireandforget (bool): Whether we should return immediately after sending the command. If True, return value is None.
            checkpreempt (bool): If a preempt function should be checked during execution.
            forcereload (bool): If True, then force re-load the scene before executing the task
        
        Returns:
            dict: Server response in JSON format. If fireandforget is True, then None.
        """
        if 'stamp' not in taskparameters:
            taskparameters['stamp'] = time.time()
        if slaverequestid is None:
            slaverequestid = self._slaverequestid

        command = {
            'fnname': 'RunCommand',
            'taskparams': {
                'tasktype': self.tasktype,
                'sceneparams': self._sceneparams,
                'taskparameters': taskparameters,
                'forcereload':forcereload,
            },
            'userinfo': self._userinfo,
            'slaverequestid': slaverequestid,
            'stamp': time.time(),
            'respawnopts': respawnopts,
        }
        if self._callerid is not None:
            command['callerid'] = self._callerid
            if 'callerid' not in taskparameters:
                taskparameters['callerid'] = self._callerid
        if self.tasktype == 'binpicking':
            command['fnname'] = '%s.%s' % (self.tasktype, command['fnname'])
        response = self._commandsocket.SendCommand(command, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)

        if fireandforget:
            # For fire and forget commands, no response will be available
            return None

        error = GetAPIServerErrorFromZMQ(response)
        if error is not None:
            log.warn('GetAPIServerErrorFromZMQ returned error for %r', response)
            raise error
        if response is None:
            log.warn(u'got no response from task %r', taskparameters)
            return None

        return response['output']
        
    #
    # Config
    #

    def Configure(self, configuration, timeout=None, fireandforget=None, slaverequestid=None):
        """Send a 'configure' command to the configsocket.

        Args:
            configuration (dict): The payload to send to the server. The 'command' field will be set to 'configure'.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
            fireandforget (bool, optional): If True, does not wait for the configuration to have completed.

        Returns:
            dict: The 'output' field of the server response.
        """
        configuration['command'] = 'configure'
        return self.SendConfig(configuration, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def SetLogLevel(self, componentLevels, fireandforget=None, slaverequestid=None, timeout=5):
        """Set planning log level.

        Args:
            componentLevels (dict): Mapping from component name to level name, for example {"some.specific.component": "DEBUG"}.
                                If component name is empty string, it sets the root logger.
                                If level name is empty string, it unsets the level previously set.
        """
        super(PlanningClient, self).SetLogLevel(componentLevels, timeout=timeout)
        configuration = {
            'command': 'setloglevel',
            'componentLevels': componentLevels
        }
        return self.SendConfig(configuration, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def SendConfig(self, command, slaverequestid=None, timeout=None, fireandforget=None, checkpreempt=True):
        """Sends a config command via ZMQ to the planning server.
        """
        if slaverequestid is None:
            slaverequestid = self._slaverequestid
            
        command['slaverequestid'] = slaverequestid
        if self._callerid is not None:
            command['callerid'] = self._callerid
        response = self._configsocket.SendCommand(command, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)
        if fireandforget:
            # For fire and forget commands, no response will be available
            return None

        error = GetAPIServerErrorFromZMQ(response)
        if error is not None:
            raise error
        return response['output']

    #
    # Viewer Parameters Related
    #

    def SetViewerFromParameters(self, viewerparameters, timeout=10, fireandforget=True, slaverequestid=None, **kwargs):
        viewerparameters.update(kwargs)
        return self.Configure({'viewerparameters': viewerparameters}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def MoveCameraZoomOut(self, zoommult=0.9, zoomdelta=20, timeout=10, fireandforget=True, ispan=True, slaverequestid=None, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomOut',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
            'ispan': bool(ispan)
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def MoveCameraZoomIn(self, zoommult=0.9, zoomdelta=20, timeout=10, fireandforget=True, slaverequestid=None, ispan=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomIn',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
            'ispan': bool(ispan)
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def MoveCameraLeft(self, ispan=True, panangle=5.0, pandelta=0.04, timeout=10, fireandforget=True, slaverequestid=None, **kwargs):
        viewercommand = {
            'command': 'MoveCameraLeft',
            'pandelta': float(pandelta),
            'panangle': float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def MoveCameraRight(self, ispan=True, panangle=5.0, pandelta=0.04, timeout=10, fireandforget=True, slaverequestid=None, **kwargs):
        viewercommand = {
            'command': 'MoveCameraRight',
            'pandelta': float(pandelta),
            'panangle': float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def MoveCameraUp(self, ispan=True, angledelta=3.0, pandelta=0.04, timeout=10, fireandforget=True, slaverequestid=None, **kwargs):
        viewercommand = {
            'command': 'MoveCameraUp',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def MoveCameraDown(self, ispan=True, angledelta=3.0, pandelta=0.04, timeout=10, fireandforget=True, slaverequestid=None, **kwargs):
        viewercommand = {
            'command': 'MoveCameraDown',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def MoveCameraPointOfView(self, pointOfViewName, timeout=10, fireandforget=True, slaverequestid=None, **kwargs):
        """
        Sends a command that moves the camera to one of the following point of view names:
        +x, -x, +y, -y, +z, -z.
        For each point of view, the camera will be aligned to the scene's bounding box center, and the whole scene will be visible. The camera will look at the 
        scene from the opposite direction of the point of view's name's axis (for instance, the camera placed at +x will look at the scene from the -x direction).
        """
        viewercommand = {
            'command': 'MoveCameraPointOfView',
            'axis': pointOfViewName,
        }
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def SetCameraTransform(self, pose=None, transform=None, distanceToFocus=0.0, timeout=10, fireandforget=True, slaverequestid=None, **kwargs):
        """Sets the camera transform
        
        Args:
            transform: 4x4 matrix
        """
        viewercommand = {
            'command': 'SetCameraTransform',
            'distanceToFocus': float(distanceToFocus),
        }
        if transform is not None:
            viewercommand['transform'] = [list(row) for row in transform]
        if pose is not None:
            viewercommand['pose'] = [float(f) for f in pose]
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def StartIPython(self, timeout=1, fireandforget=True, slaverequestid=None, **kwargs):
        configuration = {'startipython': True}
        configuration.update(kwargs)
        return self.Configure(configuration, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

    def StartRemotePDB(self, timeout=1, fireandforget=True, slaverequestid=None, **kwargs):
        configuration = {'startremotepdb': True}
        configuration.update(kwargs)
        return self.Configure(configuration, timeout=timeout, fireandforget=fireandforget, slaverequestid=slaverequestid)

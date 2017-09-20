# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 MUJIN Inc
"""
Planning client
"""

# logging
from logging import getLogger
log = getLogger(__name__)

# system imports
from urlparse import urlparse
from urllib import quote, unquote
import os
import time
import datetime

try:
    import zmq
except ImportError:
    # cannot use zmq
    pass

from threading import Thread
import weakref

# mujin imports
from . import ControllerClientError, GetAPIServerErrorFromZMQ
from . import controllerclientbase, zmqclient
from . import ugettext as _


class PlanningControllerClient(controllerclientbase.ControllerClient):
    """mujin controller client for planning tasks
    """
    _usewebapi = True  # if True use the HTTP webapi, otherwise the zeromq webapi (internal use only)
    _sceneparams = None
    scenepk = None # the scenepk this controller is configured for
    _ctx = None  # zmq context shared among all clients
    _ctxown = None # zmq context owned by this class
    _isok = False # if False, client is about to be destroyed
    _heartbeatthread = None  # thread for monitoring controller heartbeat
    _isokheartbeat = False  # if False, then stop heartbeat monitor
    _taskstate = None  # latest task status from heartbeat message
    _commandsocket = None # zmq client to the command port
    _configsocket = None # zmq client to the config port

    def __init__(self, taskzmqport, taskheartbeatport, taskheartbeattimeout, tasktype, scenepk, usewebapi=True, ctx=None, slaverequestid=None, **kwargs):
        """logs into the mujin controller and initializes the task's zmq connection
        :param taskzmqport: port of the task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing task's zmq server if no hearbeat is received, e.g. 7
        :param tasktype: type of the task
        :param scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
        """
        super(PlanningControllerClient, self).__init__(**kwargs)
        self._slaverequestid = slaverequestid
        self._sceneparams = {}
        self._isok = True

        # task
        self.tasktype = tasktype
        self._usewebapi = usewebapi
        
        # connects to task's zmq server
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
            if self.taskheartbeatport is not None:
                self._isokheartbeat = True
                self._heartbeatthread = Thread(target=weakref.proxy(self)._RunHeartbeatMonitorThread)
                self._heartbeatthread.start()
                
        self.SetScenePrimaryKey(scenepk)
        
    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()

        if self._heartbeatthread is not None:
            self._isokheartbeat = False
            self._heartbeatthread.join()
            self._heartbeatthread = None
        if self._commandsocket is not None:
            self._commandsocket.Destroy()
            self._commandsocket = None
        if self._configsocket is not None:
            self._configsocket.Destroy()
            self._configsocket = None
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
            except:
                pass
            self._ctxown = None

        super(PlanningControllerClient, self).Destroy()
    
    def SetDestroy(self):
        self._isok = False
        self._isokheartbeat = False
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configsocket is not None:
            self._configsocket.SetDestroy()
        super(PlanningControllerClient, self).SetDestroy()

    def GetSlaveRequestId(self):
        return self._slaverequestid

    def DeleteJobs(self, usewebapi=True, timeout=5):
        """ cancels all jobs
        """
        if usewebapi:
            super(PlanningControllerClient, self).DeleteJobs(usewebapi, timeout)
        else:
            # cancel on the zmq configure
            if self._configsocket is not None:
                self._SendConfigViaZMQ({'command':'cancel'}, self._slaverequestid, timeout=timeout, fireandforget=False)
        
    
    def _RunHeartbeatMonitorThread(self, reinitializetimeout=10.0):
        while self._isok and self._isokheartbeat:
            log.info(u'subscribing to %s:%s' % (self.controllerIp, self.taskheartbeatport))
            socket = self._ctx.socket(zmq.SUB)
            socket.connect('tcp://%s:%s' % (self.controllerIp, self.taskheartbeatport))
            socket.setsockopt(zmq.SUBSCRIBE, '')
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)

            lastheartbeatts = time.time()
            while self._isokheartbeat and time.time() - lastheartbeatts < reinitializetimeout:
                socks = dict(poller.poll(50))
                if socket in socks and socks.get(socket) == zmq.POLLIN:
                    try:
                        reply = socket.recv_json(zmq.NOBLOCK)
                        if 'taskstate' in reply:
                            self._taskstate = reply['taskstate']
                            lastheartbeatts = time.time()
                        else:
                            self._taskstate = None
                    except zmq.ZMQError, e:
                        log.error('failed to receive from publisher')
                        log.error(e)
            if self._isokheartbeat:
                log.warn('%f secs since last heartbeat from controller' % (time.time() - lastheartbeatts))

    def GetPublishedTaskState(self):
        """return most recent published state. if publishing is disabled, then will return None
        """
        return self._taskstate

    def SetScenePrimaryKey(self, scenepk):
        self.scenepk = scenepk
        sceneuri = controllerclientbase.GetURIFromPrimaryKey(scenepk)
        # for now (HACK) need to set the correct scenefilename. newer version of mujin controller need only scenepk, so remove scenefilename eventually
        mujinpath = os.path.join(os.environ.get('MUJIN_MEDIA_ROOT_DIR', '/var/www/media/u'), self.controllerusername)
        scenefilename = controllerclientbase.GetFilenameFromURI(sceneuri, mujinpath)[1]
        self._sceneparams = {'scenetype': 'mujincollada', 'sceneuri': sceneuri, 'scenefilename': scenefilename, 'scale': [1.0, 1.0, 1.0]}  # TODO: set scenetype according to the scene

    #
    # Tasks related
    #

    def RunSceneTaskAsync(self, scenepk, taskpk, slaverequestid=None, fields=None, usewebapi=True, timeout=5):
        """
        :return: {'jobpk': 'xxx', 'msg': 'xxx'}
        """
        assert(usewebapi)
        if slaverequestid is None:
            slaverequestid = self._slaverequestid
        data = {
            'scenepk': scenepk,
            'target_pk': taskpk,
            'resource_type': 'task',
            'slaverequestid': slaverequestid,
        }
        status, response = self._webclient.APICall('POST', u'job/', data=data, timeout=timeout)
        assert(status == 200)
        return response

    def ExecuteTaskSync(self, scenepk, tasktype, taskparameters, slaverequestid='', timeout=None):
        '''executes task with a particular task type without creating a new task
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: if True, then cancel all previously running jobs before running this one
        '''
        # execute task
        status, response = self._webclient.APICall('GET', u'scene/%s/resultget' % (scenepk), data={
            'tasktype': tasktype,
            'taskparameters': taskparameters,
            'slaverequestid': slaverequestid,
            'timeout': timeout,
        }, timeout=timeout)
        assert(status==200)
        return response

    def _ExecuteCommandViaWebAPI(self, taskparameters, slaverequestid='', timeout=None):
        """executes command via web api
        """
        return self.ExecuteTaskSync(self.scenepk, self.tasktype, taskparameters, slaverequestid=slaverequestid, timeout=timeout)

    def _ExecuteCommandViaZMQ(self, taskparameters, slaverequestid='', timeout=None, fireandforget=None):
        command = {
            'fnname': 'RunCommand',
            'taskparams': {
                'tasktype': self.tasktype,
                'sceneparams': self._sceneparams,
                'taskparameters': taskparameters,
            },
            'userinfo': self._userinfo,
            'slaverequestid': slaverequestid,
        }
        if self.tasktype == 'binpicking':
            command['fnname'] = '%s.%s' % (self.tasktype, command['fnname'])
        response = self._commandsocket.SendCommand(command, timeout=timeout, fireandforget=fireandforget)
        
        if fireandforget:
            # for fire and forget commands, no response will be available
            return None

        error = GetAPIServerErrorFromZMQ(response)
        if error is not None:
            log.warn('GetAPIServerErrorFromZMQ returned error for %r', response)
            raise error
        if response is None:
            log.warn(u'got no response from task %r', taskparameters)
            return None
        
        return response['output']

    def ExecuteCommand(self, taskparameters, usewebapi=None, slaverequestid=None, timeout=None, fireandforget=None):
        """executes command with taskparameters
        :param taskparameters: task parameters in json format
        :param timeout: timeout in seconds for web api call
        :param fireandforget: whether we should return immediately after sending the command
        :return: return the server response in json format
        """
        if not 'timestamp' in taskparameters:
            taskparameters['timestamp'] = int(time.time()*1000.0)
        log.verbose(u'Executing task with parameters: %r', taskparameters)
        if slaverequestid is None:
            slaverequestid = self._slaverequestid

        if usewebapi is None:
            usewebapi = self._usewebapi

        if usewebapi:
            return self._ExecuteCommandViaWebAPI(taskparameters, timeout=timeout, slaverequestid=slaverequestid)
        else:
            return self._ExecuteCommandViaZMQ(taskparameters, timeout=timeout, slaverequestid=slaverequestid, fireandforget=fireandforget)

    #
    # Config
    #

    def Configure(self, configuration, usewebapi=None, timeout=None, fireandforget=None):
        configuration['command'] = 'configure'
        return self.SendConfig(configuration, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SendConfig(self, command, usewebapi=None, slaverequestid=None, timeout=None, fireandforget=None):
        log.verbose(u'Send config: %r', command)
        if slaverequestid is None:
            slaverequestid = self._slaverequestid

        return self._SendConfigViaZMQ(command, slaverequestid=slaverequestid, timeout=timeout, fireandforget=fireandforget)

    def _SendConfigViaZMQ(self, command, slaverequestid='', timeout=None, fireandforget=None):
        command['slaverequestid'] = slaverequestid
        response = self._configsocket.SendCommand(command, timeout=timeout, fireandforget=fireandforget)
        if fireandforget:
            # for fire and forget commands, no response will be available
            return None

        error = GetAPIServerErrorFromZMQ(response)
        if error is not None:
            raise error
        return response['output']

    #
    # Viewer Parameters Related
    #

    def SetViewerFromParameters(self, viewerparameters, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewerparameters.update(kwargs)
        return self.Configure({'viewerparameters': viewerparameters}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraZoomOut(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, ispan=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomOut',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
            'ispan': bool(ispan)
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraZoomIn(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, ispan=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomIn',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
            'ispan': bool(ispan)
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraLeft(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraLeft',
            'pandelta': float(pandelta),
            'panangle': float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraRight(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraRight',
            'pandelta': float(pandelta),
            'panangle':float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraUp(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraUp',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraDown(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraDown',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def SetCameraTransform(self, pose=None, transform=None, distanceToFocus=0.0, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        """sets the camera transform
        :param transform: 4x4 matrix
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
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

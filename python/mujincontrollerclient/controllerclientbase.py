# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
"""
Mujin controller client base
"""
from urlparse import urlparse
from urllib import quote, unquote
import os
import base64
from numpy import fromstring, uint32, unique


# logging
from logging import getLogger
log = getLogger(__name__)

# system imports
import time
import datetime

try:
    import ujson as json
except ImportError:
    import json

try:
    import zmq
except ImportError:
    # cannot use zmq
    pass

from threading import Thread
import weakref

# mujin imports
from . import ControllerClientError, GetAPIServerErrorFromZMQ
from . import controllerclientraw, zmqclient
from . import ugettext as _

# the outside world uses this specifier to signify a '#' specifier. This is needed
# because '#' in URL parsing is a special role
id_separator = u'@'


def GetFilenameFromURI(uri, mujinpath):
    """returns the filesystem path that the URI points to.
    :param uri: points to mujin:/ resource

    example:

      GetFilenameFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae',u'/var/www/media/u/testuser')
      returns: (ParseResult(scheme=u'mujin', netloc='', path=u'/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae', params='', query='', fragment=''), u'/var/www/media/u/testuser/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
    """
    index = uri.find(id_separator)
    if index >= 0:
        res = urlparse(uri[:index])
    else:
        res = urlparse(uri)
    if res.scheme != 'mujin':
        raise ControllerClientError(_('Only mujin: sceheme supported of %s') % uri)
    if len(res.path) == 0 or res.path[0] != '/':
        raise ControllerClientError(_('path is not absolute on URI %s') % uri)
    if os.path.exists(res.path):
        # it's already an absolute path, so return as is. making sure user can read from this path is up to the filesystem permissions
        return res, res.path
    else:
        return res, os.path.join(mujinpath, res.path[1:])


def GetURIFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode URL.
    If pk is a unicode object, will use inside url as is, otherwise will decode

    example:

      GetURIFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122')
      returns: u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae'
    """
    pkunicode = GetUnicodeFromPrimaryKey(pk)
    # check if separator is present
    index = pkunicode.find(id_separator)
    if index >= 0:
        basefilename = pkunicode[0:index]
        if len(os.path.splitext(basefilename)[1]) == 0:
            # no extension present in basefilename, so default to mujin.dae
            basefilename += u'.mujin.dae'
        return u'mujin:/' + basefilename + pkunicode[index:]
    if len(os.path.splitext(pkunicode)[1]) == 0:
        # no extension present in basefilename, so default to mujin.dae
        pkunicode += u'.mujin.dae'
    return u'mujin:/' + pkunicode


def GetUnicodeFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode string.
    If pk is a unicode object, will return the string as is.

    example:

      GetUnicodeFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122')
      returns: u'\u691c\u8a3c\u52d5\u4f5c1_121122'
    """
    if not isinstance(pk, unicode):
        return unicode(unquote(str(pk)), 'utf-8')
    else:
        return pk


def GetPrimaryKeyFromURI(uri):
    """
    example:

      GetPrimaryKeyFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
      returns u'%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122'
    """
    res = urlparse(unicode(uri))
    path = res.path[1:]
    return quote(path.encode('utf-8'), '')


class ControllerClientBase(object):
    """mujin controller client base
    """
    _usewebapi = True  # if True use the HTTP webapi, otherwise the zeromq webapi (internal use only)
    _sceneparams = None
    _webclient = None
    scenepk = None # the scenepk this controller is configured for
    _ctx = None  # zmq context shared among all clients
    _ctxown = None # zmq context owned by this class
    _isok = False # if False, client is about to be destroyed
    _heartbeatthread = None  # thread for monitoring controller heartbeat
    _isokheartbeat = False  # if False, then stop heartbeat monitor
    _taskstate = None  # latest task status from heartbeat message
    _userinfo = None # a dict storing user info, like locale
    _commandsocket = None # zmq client to the command port
    _configsocket = None # zmq client to the config port

    def __init__(self, controllerurl, controllerusername, controllerpassword, taskzmqport, taskheartbeatport, taskheartbeattimeout, tasktype, scenepk, usewebapi=True, ctx=None, slaverequestid=None):
        """logs into the mujin controller and initializes the task's zmq connection
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param taskzmqport: port of the task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing task's zmq server if no hearbeat is received, e.g. 7
        :param tasktype: type of the task
        :param scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
        """
        self._slaverequestid = slaverequestid
        self._sceneparams = {}
        self._isok = True
        self._userinfo = {
            'username': controllerusername,
            'locale': os.environ.get('LANG', ''),
        }

        # task
        self.tasktype = tasktype
        self._usewebapi = usewebapi
        # logs in via web api
        self.controllerurl = controllerurl
        self.controllerIp = controllerurl[len('http://'):].split(":")[0]
        if len(controllerurl[len('http://'):].split(":")) > 1:
            self.controllerPort = controllerurl[len('http://'):].split(":")[1]
        else:
            self.controllerPort = 80
        self.controllerusername = controllerusername
        self.controllerpassword = controllerpassword
        self._webclient = controllerclientraw.ControllerWebClient(controllerurl, controllerusername, controllerpassword)

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

        if self._webclient is not None:
            self._webclient.Destroy()
            self._webclient = None
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
    
    def SetDestroy(self):
        self._isok = False
        if self._webclient is not None:
            self._webclient.SetDestroy()
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configsocket is not None:
            self._configsocket.SetDestroy()
    
    def SetLocale(self, locale):
        self._userinfo['locale'] = locale
        self._webclient.SetLocale(locale)
    
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

    def RestartController(self):
        """ restarts controller
        """
        self._webclient.Request('POST', '/restartserver/', timeout=1)
        # no reason to check response since it's probably an error (server is restarting after all)

    def IsLoggedIn(self):
        return self._webclient.IsLoggedIn()

    def Login(self, timeout=5):
        """Force webclient to login if it is not currently logged in. Useful for checking that the credential works.
        """
        self._webclient.Login(timeout=timeout)

    #
    # Scene related
    #

    def UploadSceneFile(self, f):
        """uploads a file managed by file handle f
        
        """
        # note that /fileupload does not have trailing slash for some reason
        response = self._webclient.Request('POST', '/fileupload', files={'files[]': f})
        if response.status_code != 200:
            raise ControllerClientError(response.content)
        
        try:
            content = json.loads(response.content)
        except ValueError:
            raise ControllerClientError(response.content)
        
        return content['filename']


    def SetScenePrimaryKey(self, scenepk):
        self.scenepk = scenepk
        sceneuri = GetURIFromPrimaryKey(scenepk)
        # for now (HACK) need to set the correct scenefilename. newer version of mujin controller need only scenepk, so remove scenefilename eventually
        mujinpath = os.path.join(os.environ.get('MUJIN_MEDIA_ROOT_DIR', '/var/www/media/u'), self.controllerusername)
        scenefilename = GetFilenameFromURI(sceneuri, mujinpath)[1]
        self._sceneparams = {'scenetype': 'mujincollada', 'sceneuri': sceneuri, 'scenefilename': scenefilename, 'scale': [1.0, 1.0, 1.0]}  # TODO: set scenetype according to the scene

    def GetScenes(self, fields=None, usewebapi=True, timeout=5):
        """list all available scene on controller
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/', fields=fields, timeout=timeout, url_params={
            'limit': 0,
        })
        assert(status == 200)
        return response['objects']

    def GetScene(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/' % pk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetObject(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested object
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/' % pk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetRobot(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested robot
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'robot/%s/' % pk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    #
    # Scene related
    #

    def CreateScene(self, scenedata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/', data=scenedata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetScene(self, scenepk, scenedata, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/' % scenepk, data=scenedata, timeout=timeout)
        assert(status == 202)

    def DeleteScene(self, scenepk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/' % scenepk, timeout=timeout)
        assert(status == 204)

    #
    # InstObject related
    #

    def CreateSceneInstObject(self, scenepk, instobjectdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/%s/instobject/' % scenepk, data=instobjectdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetSceneInstObject(self, scenepk, instobjectpk, instobjectdata, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/instobject/%s/' % (scenepk, instobjectpk), data=instobjectdata, timeout=timeout)
        assert(status == 202)

    def DeleteSceneInstObject(self, scenepk, instobjectpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/instobject/%s/' % (scenepk, instobjectpk), timeout=timeout)
        assert(status == 204)

    #
    # IKParam related
    #

    def CreateObjectIKParam(self, objectpk, ikparamdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'object/%s/ikparam/' % objectpk, data=ikparamdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetObjectIKParam(self, objectpk, ikparampk, ikparamdata, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/ikparam/%s/' % (objectpk, ikparampk), data=ikparamdata, timeout=timeout)
        assert(status == 202)
        
    def DeleteObjectIKParam(self, objectpk, ikparampk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/ikparam/%s/' % (objectpk, ikparampk), timeout=timeout)
        assert(status == 204)
        
    #
    # GraspSet related
    #

    def CreateObjectGraspSet(self, objectpk, graspsetdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'object/%s/graspset/' % objectpk, data=graspsetdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetObjectGraspSet(self, objectpk, graspsetpk, graspsetdata, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), data=graspsetdata, timeout=timeout)
        assert(status == 202)

    def DeleteObjectGraspSet(self, objectpk, graspsetpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), timeout=timeout)
        assert(status == 204)

    #
    # Tools related
    #

    def CreateRobotTool(self, robotpk, tooldata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'robot/%s/tool/' % robotpk, data=tooldata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetRobotTool(self, robotpk, toolpk, tooldata, usewebapi=True, timeout=5):
        """sets the tool values via a WebAPI PUT call
        :param tooldata: key-value pairs of the data to modify on the tool
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'robot/%s/tool/%s/' % (robotpk, toolpk), data=tooldata, timeout=timeout)
        assert(status == 202)

    def DeleteRobotTool(self, robotpk, toolpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'robot/%s/tool/%s/' % (robotpk, toolpk), timeout=timeout)
        assert(status == 204)

    #
    # Attached sensors related
    #

    def CreateRobotAttachedSensor(self, robotpk, attachedsensordata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'robot/%s/attachedsensor/' % robotpk, data=attachedsensordata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetRobotAttachedSensor(self, robotpk, attachedsensorpk, attachedsensordata, usewebapi=True, timeout=5):
        """sets the attachedsensor values via a WebAPI PUT call
        :param attachedsensordata: key-value pairs of the data to modify on the attachedsensor
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'robot/%s/attachedsensor/%s/' % (robotpk, attachedsensorpk), data=attachedsensordata, timeout=timeout)
        assert(status == 202)

    def DeleteRobotAttachedSensor(self, robotpk, attachedsensorpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'robot/%s/attachedsensor/%s/' % (robotpk, attachedsensorpk), timeout=timeout)
        assert(status == 204)

    #
    # Task related
    #

    def GetSceneTasks(self, scenepk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/task/' % scenepk, fields=fields, timeout=timeout, url_params={
            'limit': 0,
        })
        assert(status == 200)
        return response['objects']

    def GetSceneTask(self, scenepk, taskpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/task/%s/' % (scenepk, taskpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def CreateSceneTask(self, scenepk, taskdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/%s/task/' % scenepk, data=taskdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetSceneTask(self, scenepk, taskpk, taskdata, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/task/%s/' % (scenepk, taskpk), data=taskdata, timeout=timeout)
        assert(status == 202)

    def DeleteSceneTask(self, scenepk, taskpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/task/%s/' % (scenepk, taskpk), timeout=timeout)
        assert(status == 204)

    def RunSceneTaskAsync(self, scenepk, taskpk, slaverequestid=None, fields=None, usewebapi=True, timeout=5):
        """
        :return: {'jobpk': 'xxx', 'msg': 'xxx'}
        """
        assert(usewebapi)
        if slaverequestid is None:
            slaverequestid =self._slaverequestid
        data = {
            'scenepk': scenepk,
            'target_pk': taskpk,
            'resource_type': 'task',
            'slaverequestid': slaverequestid,
        }
        status, response = self._webclient.APICall('POST', u'job/', data=data, timeout=timeout)
        assert(status == 200)
        return response

    #
    # Result related
    #

    def GetResult(self, resultpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'planningresult/%s/' % resultpk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetResultProgram(self, resultpk, programtype=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        params = {'format': 'dat'}
        if programtype is not None and len(programtype) > 0:
            params['type'] = programtype
        # custom http call because APICall currently only supports json
        response = self._webclient.Request('GET', u'/api/v1/planningresult/%s/program/' % resultpk, params=params, timeout=timeout)
        assert(response.status_code == 200)
        return response.content

    def SetResult(self, resultpk, resultdata, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'planningresult/%s/' % resultpk, data=resultdata, timeout=timeout)
        assert(status == 202)

    def DeleteResult(self, resultpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'planningresult/%s/' % resultpk, timeout=timeout)
        assert(status == 204)

    #
    # Job related
    #

    def GetJobs(self, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'job/', fields=fields, timeout=timeout, url_params={
            'limit': 0,
        })
        assert(status == 200)
        return response['objects']

    def DeleteJob(self, jobpk, usewebapi=True, timeout=5):
        """ cancels the job with the corresponding jobk
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'job/%s/' % jobpk, timeout=timeout)
        assert(status == 204)

    def DeleteJobs(self, usewebapi=True, timeout=5):
        """ cancels all jobs
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'job/', timeout=timeout)
        assert(status == 204)

    #
    # Geometry related
    #
    
    def GetObjectGeometry(self, objectpk, usewebapi=True, timeout=5):
        """ return a list of geometries (a dictionary with key: positions, indices)) of given object
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/geometry/' % objectpk, timeout=timeout)
        assert(status == 200)
        geometries = []
        for encodedGeometry in response['geometries']:
            geometry = {}
            positions = fromstring(base64.b64decode(encodedGeometry['positions_base64']), dtype=float)
            positions.resize(len(positions) / 3, 3)
            geometry['positions'] = positions
            indices = fromstring(base64.b64decode(encodedGeometry['positions_base64']), dtype=uint32)
            indices.resize(len(indices) / 3, 3)
            geometry['indices'] = indices
            geometries.append(geometry)
        return geometries

    #
    # Instobject related
    #

    def GetSceneInstanceObjectsViaWebapi(self, scenepk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response['instobjects']

    #
    # Sensor mappings related
    #

    def GetSceneSensorMapping(self, scenepk=None, usewebapi=True, timeout=5):
        """ return the camerafullname to cameraid mapping. e.g. {'sourcecamera/ensenso_l_rectified': '150353', 'sourcecamera/ensenso_r_rectified':'150353_Right' ...}
        """
        assert(usewebapi)
        if scenepk is None:
            scenepk = self.scenepk
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, timeout=timeout)
        assert(status == 200)
        instobjects = response['instobjects']
        sensormapping = {}
        for instobject in instobjects:
            if len(instobject['attachedsensors']) > 0:
                status, response = self._webclient.APICall('GET', u'robot/%s/attachedsensor/' % instobject['object_pk'])
                assert (status == 200)
                for attachedsensor in response['attachedsensors']:
                    camerafullname = instobject['name'] + '/' + attachedsensor['name']
                    if 'hardware_id' in attachedsensor['sensordata']:
                        sensormapping[camerafullname] = attachedsensor['sensordata']['hardware_id']
                    else:
                        sensormapping[camerafullname] = None
                        log.warn(u'attached sensor %s/%s does not have hardware_id', instobject['name'], attachedsensor.get('name',None))
        return sensormapping

    def SetSceneSensorMapping(self, sensormapping, scenepk=None, usewebapi=True, timeout=5):
        """
        :param sensormapping: the camerafullname to cameraid mapping. e.g. {'sourcecamera/ensenso_l_rectified': '150353', 'sourcecamera/ensenso_r_rectified':'150353_Right' ...}
        """
        assert(usewebapi)
        if scenepk is None:
            scenepk = self.scenepk
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, timeout=timeout)
        assert(status == 200)
        instobjects = response['instobjects']
        cameracontainernames = unique([camerafullname.split('/')[0] for camerafullname in sensormapping.keys()])
        for instobject in instobjects:
            if len(instobject['attachedsensors']) > 0 and instobject['name'] in cameracontainernames:
                cameracontainerpk = instobject['object_pk']
                status, response = self._webclient.APICall('GET', u'robot/%s/attachedsensor/' % cameracontainerpk)
                assert (status == 200)
                for attachedsensor in response['attachedsensors']:
                    camerafullname = instobject['name'] + '/' + attachedsensor['name']
                    cameraid = attachedsensor['sensordata'].get('hardware_id', None)
                    sensorpk = attachedsensor['pk']
                    if camerafullname in sensormapping.keys():
                        if cameraid != sensormapping[camerafullname]:
                            status, response = self._webclient.APICall('PUT', u'robot/%s/attachedsensor/%s' % (cameracontainerpk, sensorpk), data={'sensordata': {'hardware_id': str(sensormapping[camerafullname])}})

    #
    # Tasks related
    #

    def ExecuteTaskSync(self, scenepk, tasktype, taskparameters, slaverequestid='', timeout=1000):
        '''executes task with a particular task type without creating a new task
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: if True, then cancel all previously running jobs before running this one
        '''
        # execute task
        status, response = self._webclient.APICall('GET', u'scene/%s/resultget' % (scenepk), data={'tasktype': tasktype, 'taskparameters': taskparameters, 'slaverequestid': slaverequestid}, timeout=timeout)
        assert(status==200)
        return response

    def _ExecuteCommandViaWebAPI(self, taskparameters, slaverequestid='', timeout=3000):
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
            raise error
        return response['output']

    def ExecuteCommand(self, taskparameters, usewebapi=None, slaverequestid=None, timeout=None, fireandforget=None):
        """executes command with taskparameters
        :param taskparameters: task parameters in json format
        :param timeout: timeout in seconds for web api call
        :param fireandforget: whether we should return immediately after sending the command
        :return: return the server response in json format
        """
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
    # WebDAV related
    #
    
    def FileExists(self, path):
        """check if a file exists on server
        """
        response = self._webclient.Request('HEAD', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')))
        if response.status_code not in [200, 301, 404]:
            raise ControllerClientError(response.content)
        return response.status_code != 404
    
    def DownloadFile(self, filename):
        """downloads a file given filename

        :return: a streaming response
        """
        response = self._webclient.Request('GET', u'/u/%s/%s' % (self.controllerusername, filename), stream=True)
        if response.status_code != 200:
            raise ControllerClientError(response.content)
        
        return response

    def UploadFile(self, path, f):
        response = self._webclient.Request('PUT', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), data=f)
        if response.status_code not in [201, 201, 204]:
            raise ControllerClientError(response.content)

    def ListFiles(self, path=''):
        path = u'/u/%s/%s' % (self.controllerusername, path.rstrip('/'))
        response = self._webclient.Request('PROPFIND', path)
        if response.status_code not in [207]:
            raise ControllerClientError(response.content)

        import xml.etree.cElementTree as xml
        import email.utils

        tree = xml.fromstring(response.content)

        def prop(e, name, default=None):
            child = e.find('.//{DAV:}' + name)
            return default if child is None else child.text

        files = {}
        for e in tree.findall('{DAV:}response'):
            name = prop(e, 'href')
            assert(name.startswith(path))
            name = name[len(path):].strip('/')
            size = int(prop(e, 'getcontentlength', 0))
            isdir = prop(e, 'getcontenttype', '') == 'httpd/unix-directory'
            modified = email.utils.parsedate(prop(e, 'getlastmodified', ''))
            if modified is not None:
                modified = datetime.datetime(*modified[:6])
            files[name] = {
                'name': name,
                'size': size,
                'isdir': isdir,
                'modified': modified,
            }

        return files

    def DeleteFile(self, path):
        response = self._webclient.Request('DELETE', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')))
        if response.status_code not in [204, 404]:
            raise ControllerClientError(response.content)

    def DeleteDirectory(self, path):
        self.DeleteFile(path)

    def MakeDirectory(self, path):
        response = self._webclient.Request('MKCOL', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')))
        if response.status_code not in [201, 301, 405]:
            raise ControllerClientError(response.content)

    def MakeDirectories(self, path):
        parts = []
        for part in path.strip('/').split('/'):
            parts.append(part)
            self.MakeDirectory('/'.join(parts))


    #
    # Viewer Parameters Related
    #
    def SetViewerFromParameters(self, viewerparameters, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewerparameters.update(kwargs)
        return self.Configure({'viewerparameters': viewerparameters}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraZoomOut(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomOut',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraZoomIn(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomIn',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
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

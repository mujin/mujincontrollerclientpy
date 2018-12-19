# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
"""
Mujin controller client
"""

# logging
from logging import getLogger
log = getLogger(__name__)

# system imports
import sys
if sys.version_info[0]<3:
    from urlparse import urlparse, urlunparse
    from urllib import quote, unquote
else:
    from urllib.parse import urlparse, urlunparse, quote, unquote
import os
import datetime
import base64
from numpy import fromstring, uint32

try:
    import ujson as json
except ImportError:
    import json

# mujin imports
from . import ControllerClientError
from . import controllerclientraw
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
    if len(res.scheme) > 0 and res.scheme != 'mujin':
        log.warn(_('Only mujin: sceheme supported of %s') % uri)
    path = res.path[1:]

    return quote(path.encode('utf-8'), '')


def FormatHTTPDate(dt):
    """Return a string representation of a date according to RFC 1123 (HTTP/1.1).

    The supplied date must be in UTC.
    """
    weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][dt.weekday()]
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][dt.month - 1]
    return '%s, %02d %s %04d %02d:%02d:%02d GMT' % (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)


class ControllerClient(object):
    """mujin controller client base
    """
    _webclient = None
    _userinfo = None # a dict storing user info, like locale

    controllerurl = '' # url to controller
    controllerusername = '' # username to login with
    controllerpassword = '' # password to login with

    controllerIp = '' # hostname of the controller web server
    controllerPort = 80 # port of the controller web server

    def __init__(self, controllerurl='http://127.0.0.1', controllerusername='', controllerpassword=''):
        """logs into the mujin controller
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        """

        # parse controllerurl
        scheme, netloc, path, params, query, fragment = urlparse(controllerurl)

        # parse any credential in the url
        if '@' in netloc:
            creds, netloc = netloc.rsplit('@', 1)
            self.controllerusername, self.controllerpassword = creds.split(':', 1)

        # parse ip (hostname really) and port
        self.controllerIp = netloc.split(':', 1)[0]
        self.controllerPort = 80
        if ':' in netloc:
            hostname, port = netloc.split(':')
            self.controllerIp = hostname
            self.controllerPort = int(port)

        self.controllerurl = urlunparse((scheme, netloc, '', '', '', ''))
        self.controllerusername = controllerusername or self.controllerusername
        self.controllerpassword = controllerpassword or self.controllerpassword

        self._userinfo = {
            'username': self.controllerusername,
            'locale': os.environ.get('LANG', ''),
        }
        self._webclient = controllerclientraw.ControllerWebClient(self.controllerurl, self.controllerusername, self.controllerpassword)
        
    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()

        if self._webclient is not None:
            self._webclient.Destroy()
            self._webclient = None
    
    def SetDestroy(self):
        if self._webclient is not None:
            self._webclient.SetDestroy()
    
    def SetLocale(self, locale):
        self._userinfo['locale'] = locale
        self._webclient.SetLocale(locale)

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

    def Ping(self, usewebapi=True, timeout=5):
        """Sends a dummy HEAD request to api endpoint
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('HEAD', '', timeout=timeout)
        assert(status == 200)

    #
    # Scene related
    #

    def UploadSceneFile(self, f, timeout=5):
        """uploads a file managed by file handle f
        
        """
        # note that /fileupload does not have trailing slash for some reason
        response = self._webclient.Request('POST', '/fileupload', files={'files[]': f}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(response.content.decode('utf-8'))
        
        try:
            content = json.loads(response.content)
        except ValueError:
            raise ControllerClientError(response.content.decode('utf-8'))
        
        return content['filename']

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

    def SetObject(self, pk, objectdata, fields=None, usewebapi=True, timeout=5):
        """do partial update on object resource
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/' % pk, data=objectdata, fields=fields, timeout=timeout)
        assert(status == 202)

    def GetRobot(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested robot
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'robot/%s/' % pk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def SetRobot(self, pk, robotdata, fields=None, usewebapi=True, timeout=5):
        """do partial update on robot resource
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'robot/%s/' % pk, data=robotdata, fields=fields, timeout=timeout)
        assert(status == 202)

    #
    # Scene related
    #

    def CreateScene(self, scenedata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/', data=scenedata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetScene(self, scenepk, scenedata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/' % scenepk, data=scenedata, fields=fields, timeout=timeout)
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

    def GetSceneInstObjects(self, scenepk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response['objects']
    
    def GetSceneInstObject(self, scenepk, instobjectpk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/%s' % (scenepk, instobjectpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response
    
    def SetSceneInstObject(self, scenepk, instobjectpk, instobjectdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/instobject/%s/' % (scenepk, instobjectpk), data=instobjectdata, fields=fields, timeout=timeout)
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

    def SetObjectIKParam(self, objectpk, ikparampk, ikparamdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/ikparam/%s/' % (objectpk, ikparampk), data=ikparamdata, fields=fields, timeout=timeout)
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

    def SetObjectGraspSet(self, objectpk, graspsetpk, graspsetdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), data=graspsetdata, fields=fields, timeout=timeout)
        assert(status == 202)

    def DeleteObjectGraspSet(self, objectpk, graspsetpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), timeout=timeout)
        assert(status == 204)

    #
    # Link related
    #

    def CreateObjectLink(self, objectpk, linkdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'object/%s/link/' % objectpk, data=linkdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetObjectLink(self, objectpk, linkpk, linkdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/link/%s/' % (objectpk, linkpk), data=linkdata, fields=fields, timeout=timeout)
        assert(status == 202)

    def DeleteObjectLink(self, objectpk, linkpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/link/%s/' % (objectpk, linkpk), timeout=timeout)
        assert(status == 204)

    #
    # Attachment related
    #

    def CreateObjectAttachment(self, objectpk, attachmentdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'object/%s/attachment/' % objectpk, data=attachmentdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetObjectAttachment(self, objectpk, attachmentpk, attachmentdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/attachment/%s/' % (objectpk, attachmentpk), data=attachmentdata, fields=fields, timeout=timeout)
        assert(status == 202)

    def DeleteObjectAttachment(self, objectpk, attachmentpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/attachment/%s/' % (objectpk, attachmentpk), timeout=timeout)
        assert(status == 204)

    #
    # Geometry related
    #

    def CreateObjectGeometry(self, objectpk, geometrydata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'object/%s/geometry/' % objectpk, data=geometrydata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetObjectGeometry(self, objectpk, geometrypk, geometrydata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/geometry/%s/' % (objectpk, geometrypk), data=geometrydata, fields=fields, timeout=timeout)
        assert(status == 202)

    def SetObjectGeometryMesh(self, objectpk, geometrypk, data, formathint='stl', unit='mm', usewebapi=True, timeout=5):
        """upload binary file content of a cad file to be set as the mesh for the geometry
        """
        assert(usewebapi)
        assert(formathint == 'stl') # for now, only support stl

        headers = {'Content-Type': 'application/sla'}
        url_params = {'unit': unit}
        status, response = self._webclient.APICall('PUT', u'object/%s/geometry/%s/' % (objectpk, geometrypk), url_params=url_params, data=data, headers=headers, timeout=timeout)
        assert(status == 202)

    def DeleteObjectGeometry(self, objectpk, geometrypk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/geometry/%s/' % (objectpk, geometrypk), timeout=timeout)
        assert(status == 204)

    def GetObjectGeometries(self, objectpk, mesh=False, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        url_params = {}
        if mesh:
            url_params['mesh'] = '1'
        status, response = self._webclient.APICall('GET', u'object/%s/geometry/' % objectpk, url_params=url_params, fields=fields, timeout=timeout)
        assert(status == 200)
        return response['geometries']

    #
    # Object Tools related
    #
    def GetRobotTools(self, robotpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'robot/%s/tool/' % robotpk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response['tools']
    
    def GetRobotTool(self, robotpk, toolpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'robot/%s/tool/%s/' % (robotpk, toolpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response
    
    def CreateRobotTool(self, robotpk, tooldata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'robot/%s/tool/' % robotpk, data=tooldata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetRobotTool(self, robotpk, toolpk, tooldata, fields=None, usewebapi=True, timeout=5):
        """sets the tool values via a WebAPI PUT call
        :param tooldata: key-value pairs of the data to modify on the tool
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'robot/%s/tool/%s/' % (robotpk, toolpk), data=tooldata, fields=fields, timeout=timeout)
        assert(status == 202)

    def DeleteRobotTool(self, robotpk, toolpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'robot/%s/tool/%s/' % (robotpk, toolpk), timeout=timeout)
        assert(status == 204)

    #
    # InstObject Tools related
    #
    
    def GetInstRobotTools(self, scenepk, instobjectpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/%s/tool/' % (scenepk, instobjectpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response['tools']

    def GetInstRobotTool(self, scenepk, instobjectpk, toolpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/%s/tool/%s' % (scenepk, instobjectpk, toolpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response
    
    def CreateInstRobotTool(self, scenepk, instobjectpk, tooldata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/%s/instobject/%s/tool/' % (scenepk, instobjectpk), data=tooldata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response
    
    def SetInstRobotTool(self, scenepk, instobjectpk, toolpk, tooldata, fields=None, usewebapi=True, timeout=5):
        """sets the tool values via a WebAPI PUT call
        :param tooldata: key-value pairs of the data to modify on the tool
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/instobject/%s/tool/%s/' % (scenepk, instobjectpk, toolpk), data=tooldata, fields=fields, timeout=timeout)
        assert(status == 202)
    
    def DeleteInstRobotTool(self, scenepk, instobjectpk, toolpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/instobject/%s/tool/%s/' % (scenepk, instobjectpk, toolpk), timeout=timeout)
        assert(status == 204)
    
    #
    # Attached sensors related
    #

    def CreateRobotAttachedSensor(self, robotpk, attachedsensordata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'robot/%s/attachedsensor/' % robotpk, data=attachedsensordata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetRobotAttachedSensor(self, robotpk, attachedsensorpk, attachedsensordata, fields=None, usewebapi=True, timeout=5):
        """sets the attachedsensor values via a WebAPI PUT call
        :param attachedsensordata: key-value pairs of the data to modify on the attachedsensor
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'robot/%s/attachedsensor/%s/' % (robotpk, attachedsensorpk), data=attachedsensordata, fields=fields, timeout=timeout)
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

    def SetSceneTask(self, scenepk, taskpk, taskdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/task/%s/' % (scenepk, taskpk), data=taskdata, fields=fields, timeout=timeout)
        assert(status == 202)

    def DeleteSceneTask(self, scenepk, taskpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/task/%s/' % (scenepk, taskpk), timeout=timeout)
        assert(status == 204)



    #
    # Result related
    #

    def GetResult(self, resultpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'planningresult/%s/' % resultpk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetBinpickingResult(self, resultpk, fields=None, usewebapi=True, timeout=5):
        assert(UserWarning)
        status, response = self._webclient.APICall('GET', u'binpickingresult/%s' % resultpk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetResultProgram(self, resultpk, programtype=None, format='dat', usewebapi=True, timeout=5):
        assert(usewebapi)
        params = {'format': format}
        if programtype is not None and len(programtype) > 0:
            params['type'] = programtype
        # custom http call because APICall currently only supports json
        response = self._webclient.Request('GET', u'/api/v1/planningresult/%s/program/' % resultpk, params=params, timeout=timeout)
        assert(response.status_code == 200)
        return response.content

    def SetResult(self, resultpk, resultdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'planningresult/%s/' % resultpk, data=resultdata, fields=fields, timeout=timeout)
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
        # cancel on the zmq configure socket first
        
        if usewebapi:
            status, response = self._webclient.APICall('DELETE', u'job/', timeout=timeout)
            assert(status == 204)
        
    #
    # Geometry related
    #
    
    def GetObjectGeometry(self, objectpk, usewebapi=True, timeout=5):
        """ return a list of geometries (a dictionary with key: positions, indices)) of given object
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/scenejs/' % objectpk, timeout=timeout)
        assert(status == 200)
        geometries = []
        for encodedGeometry in response['geometries']:
            geometry = {}
            positions = fromstring(base64.b64decode(encodedGeometry['positions_base64']), dtype=float)
            positions.resize(len(positions) / 3, 3)
            geometry['positions'] = positions
            indices = fromstring(base64.b64decode(encodedGeometry['indices_base64']), dtype=uint32)
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
        return response['objects']

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
        instobjects = response['objects']
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
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, url_params={'limit': 0}, fields='attachedsensors,object_pk,name', timeout=timeout)
        assert(status == 200)
        instobjects = response['objects']
        cameracontainernames = set([camerafullname.split('/')[0] for camerafullname in sensormapping.keys()])
        sensormapping = dict(sensormapping)
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
                        del sensormapping[camerafullname]
        if sensormapping:
            raise ControllerClientError(_('some sensors are not found in scene: %r') % sensormapping.keys())

    #
    # WebDAV related
    #
    
    def FileExists(self, path, timeout=5):
        """check if a file exists on server
        """
        response = self._webclient.Request('HEAD', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), timeout=timeout)
        if response.status_code not in [200, 301, 404]:
            raise ControllerClientError(response.content.decode('utf-8'))
        return response.status_code != 404

    def ConstructFileFullURL(self, filename):
        """construct full url to file including credentials
        """
        scheme, netloc, path, params, query, fragment = urlparse(self.controllerurl)
        return urlunparse((
            scheme,
            '%s:%s@%s' % (self.controllerusername, self.controllerpassword, netloc),
            '/u/%s/%s' % (self.controllerusername, filename),
            '',
            '',
            '',
        ))

    def DownloadFile(self, filename, ifmodifiedsince=None, timeout=5):
        """downloads a file given filename

        :return: a streaming response
        """
        headers = {}
        if ifmodifiedsince:
            headers['If-Modified-Since'] = FormatHTTPDate(ifmodifiedsince)
        response = self._webclient.Request('GET', u'/u/%s/%s' % (self.controllerusername, filename), headers=headers, stream=True, timeout=timeout)
        if ifmodifiedsince and response.status_code == 304:
            return response
        if response.status_code != 200:
            raise ControllerClientError(response.content.decode('utf-8'))
        return response

    def UploadFile(self, path, f, timeout=5):
        response = self._webclient.Request('PUT', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), data=f, timeout=timeout)
        if response.status_code not in [201, 201, 204]:
            raise ControllerClientError(response.content.decode('utf-8'))

    def ListFiles(self, path='', depth=None, timeout=5):
        """
        List files and their properties using webdav
        :param path: root path, result will include this path and its children (if depth is set to 1 or infinity)
        :param depth: 0, 1, or None (infinity)
        """
        path = u'/u/%s/%s' % (self.controllerusername, path.rstrip('/'))
        if depth is None:
            depth = 'infinity'
        response = self._webclient.Request('PROPFIND', path, headers={'Depth': str(depth)}, timeout=timeout)
        if response.status_code not in [207]:
            raise ControllerClientError(response.content.decode('utf-8'))

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
            # webdav returns quoted utf-8 filenames, so we decode here to unicode
            name = unquote(name[len(path):].strip('/')).decode('utf-8')
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

    def DeleteFile(self, path, timeout=5):
        response = self._webclient.Request('DELETE', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), timeout=timeout)
        if response.status_code not in [204, 404]:
            raise ControllerClientError(response.content.decode('utf-8'))

    def DeleteDirectory(self, path, timeout=5):
        self.DeleteFile(path, timeout=timeout)

    def MakeDirectory(self, path, timeout=5):
        response = self._webclient.Request('MKCOL', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), timeout=timeout)
        if response.status_code not in [201, 301, 405]:
            raise ControllerClientError(response.content.decode('utf-8'))

    def MakeDirectories(self, path, timeout=5):
        parts = []
        for part in path.strip('/').split('/'):
            parts.append(part)
            self.MakeDirectory('/'.join(parts), timeout=timeout)

    def RunMotorControlTuningFrequencyTest(self, jointName, amplitude, freqMin, freqMax, timeout=10, usewebapi=False, **kwargs):
        """runs frequency test on specified joint and returns result
        """
        taskparameters = {
            'command': 'RunMotorControlTuningFrequencyTest',
            'jointName': jointName,
            'freqMin': freqMin,
            'freqMax': freqMax,
            'amplitude': amplitude
         }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunMotorControlTuningStepTest(self, jointName, amplitude, timeout=10, usewebapi=False, **kwargs):
        """runs step response test on specified joint and returns result
        """
        taskparameters = {
            'command': 'RunMotorControlTuningStepTest',
            'jointName': jointName,
            'amplitude': amplitude
        }
        taskparameters.update(kwargs)
        log.warn('sending taskparameters=%r', taskparameters)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def RunMotorControlTuningMaximulLengthSequence(self, jointName, amplitude, timeout=10, usewebapi=False, **kwargs):
        """runs maximum length sequence test on specified joint and returns result
        """
        taskparameters = {
            'command': 'RunMotorControlTuningMaximulLengthSequence',
            'jointName': jointName,
            'amplitude': amplitude
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
        
    def GetMotorControlParameterSchema(self, usewebapi=False, timeout=10, **kwargs):
        """Gets motor control parameter schema
        """
        taskparameters = {
            'command': 'GetMotorControlParameterSchema',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def GetMotorControlParameter(self, jointName, parameterName, usewebapi=False, timeout=10, **kwargs):
        """Gets motor control parameters as name-value dict
        """
        taskparameters = {
            'command': 'GetMotorControlParameter',
            'jointName' : jointName,
            'parameterName' : parameterName
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetMotorControlParameters(self, usewebapi=False, timeout=10, **kwargs):
        """Gets cached motor control parameters as name-value dict
        """
        taskparameters = {
            'command': 'GetMotorControlParameters'
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def SetMotorControlParameter(self, jointName, parameterName, parameterValue, timeout=10, usewebapi=False, **kwargs):
        """Sets motor control parameter
        """
        taskparameters = {
            'command': 'SetMotorControlParameter',
            'jointName': jointName,
            'parameterName': parameterName,
            'parameterValue': parameterValue
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    #
    # Log related
    #

    def GetUserLog(self, category, level='DEBUG', keyword=None, limit=None, cursor=None, includecursor=False, forward=False, timeout=2):
        """ restarts controller
        """
        params = {
            'keyword': (keyword or '').strip(),
            'cursor': (cursor or '').strip(),
            'includecursor': 'true' if includecursor else 'false',
            'forward': 'true' if forward else 'false',
            'limit': str(limit or 0),
            'level': level,
        }

        response = self._webclient.Request('GET', '/log/user/%s/' % category, params=params, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to retrieve user log, status code is %d') % response.status_code)
        return json.loads(response.content)

    #
    # Query list of scenepks based on barcdoe field
    #

    def QueryScenePKsByBarcodes(self, barcodes, timeout=2):
        response = self._webclient.Request('GET', '/query/barcodes/', params={'barcodes': ','.join(barcodes)})
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to query scenes based on barcode, status code is %d') % response.status_code)
        return json.loads(response.content)
    

# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 MUJIN Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 
import httplib2
from httplib2 import Http
from urllib import urlencode, quote
import os, sys, re, time, shutil
import logging
import socket
log = logging.getLogger(__name__)

try:
    import simplejson as json
except ImportError:
    import json

from traceback import format_exc

from . import APIServerError, FluidPlanningError, BinPickingError, HandEyeCalibrationError

#import webdav
#from webdav import WebdavClient

class Configuration(object):
    BASE_CONTROLLER_URL = u'http://localhost:8000'
    BASE_WEBDAV_URL = u'http://localhost:8000'
    USERNAME = 'testuser2'
    PASSWORD = 'pass'
    
config = Configuration()

g_HTTP = None
g_HTTPHeaders = None

#media_root = os.path.join(os.environ['MUJIN_MEDIA_ROOT_DIR'], config.USERNAME)

class DictContainerObject:
    """Converts a python dictionary to a python object

    .. code-block:: python

      >>> args = {'a': 1, 'b': 2}
      >>> s = Struct(**args)
      >>> s
      <__main__.Struct instance at 0x01D6A738>
      >>> s.a
      1
      >>> s.b
      2

    """
    def __init__(self, **entries): 
        self.__dict__.update(entries)

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __setitem__(self, key, value):
        return self.__dict__.__setitem__(key, value)

    def __delitem__(self, key):
        return self.__dict__.__delitem__(key)

    def __contains__(self, item):
        return item in self.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        elif isinstance(other, dict):
            return self.__dict__ == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def keys(self):
        return self.__dict__.keys()

    def has_key(self, key):
        return self.__dict__.has_key(key)

def ConvertDictToObject(dictionary):
    return DictContainerObject(**dictionary)

def Login():
    global g_HTTP, g_HTTPHeaders
    csrfpattern = re.compile('csrftoken=(?P<id>[0-9a-zA-Z]*);')
    if httplib2.__version__.startswith('0.7'):
        g_HTTP = Http(".cache", disable_ssl_certificate_validation=True)
    else:
        g_HTTP = Http(".cache")

    #pw = options.pw.replace('\\','')
    g_HTTP.add_credentials(config.USERNAME, config.PASSWORD)
    try:
        responsefirst, contentfirst = g_HTTP.request(config.BASE_CONTROLLER_URL + '/login/', u'GET')
    except httplib2.RedirectLimit:
        # most likely apache2-only authentication and login page isn't needed, however need to send another GET for the csrftoken
        responsefirst, contentfirst = g_HTTP.request(config.BASE_CONTROLLER_URL + '/api/v1/', u'GET')
        sessioncookie = responsefirst.get('set-cookie')
        csrftoken = csrfpattern.findall(sessioncookie)[0]
        g_HTTPHeaders = {'Cookie': sessioncookie}
        if 'location' in responsefirst:
            g_HTTPHeaders['Referer'] = responsefirst['location']    
        # the get API CSRF token
        g_HTTPHeaders['X-CSRFToken'] = csrftoken
        g_HTTPHeaders['Content-Type'] = 'application/json; charset=UTF-8'
        if 'location' in responsefirst:
            g_HTTPHeaders['Referer'] = response['location']
        return

    firstcsrftoken = None
    if responsefirst is not None and len(csrfpattern.findall(responsefirst['set-cookie'])) != 0:
        firstcsrftoken = csrfpattern.findall(responsefirst['set-cookie'])[0]
    else:
        responsefirst, contentfirst = g_HTTP.request(config.BASE_CONTROLLER_URL + '/api/v1/', u'GET')
        firstcsrftoken = csrfpattern.findall(responsefirst['set-cookie'])[0]

    # login
    g_HTTPHeaders = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Cookie': responsefirst['set-cookie']
    }
    #headers['User-agent'] = 'Mozilla/5.0'
    g_HTTPHeaders['Referer'] = config.BASE_CONTROLLER_URL + '/login/'
    loginbody = {
        'username': config.USERNAME,
        'csrfmiddlewaretoken': firstcsrftoken,
        'password': config.PASSWORD,
        'this_is_the_login_form': '1',
        'next': '/'
    }

    response, content = g_HTTP.request(config.BASE_CONTROLLER_URL + '/login/', 'POST', headers=g_HTTPHeaders, body=urlencode(loginbody))

    if response['status'] != '302' and response['status'] != '200':
        raise ValueError(u'failed to authenticate: %r'%response)


    sessioncookie = response.get('set-cookie', responsefirst['set-cookie'])

        
    g_HTTPHeaders = {'Cookie': sessioncookie}
    if 'location' in response:
        g_HTTPHeaders['Referer'] = response['location']

    # the get API CSRF token
    response, content = g_HTTP.request(config.BASE_CONTROLLER_URL + '/api/v1/profile', 'GET', headers=g_HTTPHeaders)
    csrftoken = json.loads(content)['csrf_token']
    g_HTTPHeaders['Cookie'] += ';csrftoken=' + csrftoken
    g_HTTPHeaders['X-CSRFToken'] = csrftoken
    g_HTTPHeaders['Content-Type'] = 'application/json; charset=UTF-8'
    if 'location' in response:
        g_HTTPHeaders['Referer'] = response['location']

def RestartPlanningServer():
    if g_HTTP is None or g_HTTPHeaders is None:
        Login()
    return g_HTTP.request(config.BASE_CONTROLLER_URL + '/restartserver/', 'POST', headers=g_HTTPHeaders)
    
def IsVerified():
    if g_HTTP is None or g_HTTPHeaders is None:
        return False
    return True

# python port of the javascript API Call function
def APICall(request_type, api_url, url_params=None, fields=None, data=None):
    if g_HTTP is None or g_HTTPHeaders is None:
        Login()

    if api_url[-1] != '/':
        api_url += '/'
    url = config.BASE_CONTROLLER_URL + '/api/v1/' + api_url + '?format=json'

    if url_params is None:
        url_params = {}

    if fields is not None:
        url_params['fields'] = fields

    # implicit order by pk
    if not url_params.has_key('order_by'):
        url_params['order_by'] = 'pk'

    for param, value in url_params.iteritems():
        url += '&' + str(param) + '=' + str(value)

    if data is not None:
        if isinstance(data, DictContainerObject):
            data = data.__dict__
    else:
        data = {}

    request_type = request_type.upper()

    log.debug('%s %s', request_type, url)
    response, content = g_HTTP.request(url, request_type, body=json.dumps(data), headers=g_HTTPHeaders)

    # just return without doing anything for deletes
    if request_type == 'DELETE' and response.status == 204:
        return response.status, content

    # try to convert everything else
    else:
        error_base = u'\n\nError with %s to %s\n\nThe API call failed (status: %s)'%(request_type, url, response.status)
        try:
            content = json.loads(content)
        except ValueError:
            # either response was empty or not JSON
            raise APIServerError(u'%s, here is what came back in the request:\n%s'%(error_base, unicode(content, 'utf-8')))

        if content.has_key('traceback'):
            raise APIServerError('%s, here is the stack trace that came back in the request:\n%s'%(error_base, unicode(content['traceback'], 'utf-8')))
        
        else:
            return response.status, ConvertDictToObject(content)

def GetOrCreateTask(scenepk, taskname, tasktype=None):
    """gets or creates a task, returns its pk
    """
    status, response = APICall(u'GET', u'scene/%s/task'%scenepk, url_params={'limit':1, 'name':taskname, 'fields':'pk,tasktype'})
    assert(status==200)
    if len(response['objects']) > 0:
        if tasktype is not None:
            assert(response['objects'][0]['tasktype']==tasktype)
        return response['objects'][0]['pk']

    status, response = APICall(u'POST', u'scene/%s/task'%scenepk, url_params={'fields':'pk'}, data={"name":taskname, "tasktype":tasktype, "scenepk":scenepk})
    assert(status==201)
    return response['pk']


def ExecuteFluidTask(scenepk, taskparameters, timeout=1000):
    """
    :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
    """
    taskpk = GetOrCreateTask(scenepk, 'test0', 'fluidplanning')
    # set the task parameters
    APICall('PUT', u'scene/%s/task/%s'%(scenepk, taskpk), data={'tasktype':'fluidplanning', 'taskparameters':taskparameters})
    # just in case, delete all previous tasks
    APICall('DELETE', 'job')    
    # execute the task
    status, response = APICall('POST', u'scene/%s/task/%s'%(scenepk, taskpk))
    assert(status==200)
    # the jobpk allows us to track the job
    jobpk=response['jobpk']
    # query the task results
    status_text_prev = None
    starttime = time.time()
    try:
        while True:
            try:
                if timeout is not None and time.time()-starttime > timeout:
                    raise TimeoutError('failed to get result in time, quitting')
                
                try:
                    status, response = APICall('GET', u'job/%s'%jobpk)
                    if status == 200:
                        if status_text_prev is not None and status_text_prev != response['status_text']:
                            log.info(response['status_text'])
                        status_text_prev = response['status_text']
                        
                    jobstatus = response['status']
                except APIServerError, e:
                    # most likely job finished
                    log.warn(u'problem with requesting job: %s', e)
                    jobstatus = '2'
                if jobstatus == '2' or jobstatus == '3' or jobstatus == '4' or jobstatus == '5' or jobstatus == '8':
                    # job finished, so check for results:
                    status, response = APICall('GET', u'task/%s/result'%taskpk, url_params={'limit':1, 'optimization':'None'})
                    assert(status==200)
                    if len(response['objects']) > 0:
                        # have a response, so return!
                        jobpk = None
                        result = response['objects'][0]
                        if 'errormessage' in result and len(result['errormessage']) > 0:
                            raise FluidPlanningError(result['errormessage'])
                        
                        return result['output']
                    
            except socket.error, e:
                log.error(e)
                
            # tasks can be long, so sleep
            time.sleep(1)
            
    finally:
        if jobpk is not None:
            log.info('deleting previous job')
            APICall('DELETE', 'job/%s'%jobpk)


def ExecuteBinPickingTask(scenepk, taskparameters, timeout=1000):
    """
    :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
    """
    taskpk = GetOrCreateTask(scenepk, 'binpickingtask1', 'binpicking')
    # set the task parameters
    APICall('PUT', u'scene/%s/task/%s'%(scenepk, taskpk), data={'tasktype':'binpicking', 'taskparameters':taskparameters})
    # just in case, delete all previous tasks
    APICall('DELETE', 'job')    
    # execute the task
    #status, response = APICall('POST', u'scene/%s/task/%s'%(scenepk, taskpk))
    status, response = APICall('POST', u'job', data={'resource_type':'task', 'target_pk':taskpk})
    assert(status==200)
    # the jobpk allows us to track the job
    jobpk=response['jobpk']
    # query the task results
    status_text_prev = None
    starttime = time.time()
    try:
        while True:
            try:
                if timeout is not None and time.time()-starttime > timeout:
                    raise TimeoutError('failed to get result in time, quitting')
                
                try:
                    status, response = APICall('GET', u'job/%s'%jobpk)
                    if status == 200:
                        if status_text_prev is not None and status_text_prev != response['status_text']:
                            log.info(response['status_text'])
                        status_text_prev = response['status_text']
                        
                    jobstatus = response['status']
                except APIServerError, e:
                    # most likely job finished
                    log.warn(u'problem with requesting job: %s', e)
                    jobstatus = '2'
                if jobstatus == '2' or jobstatus == '3' or jobstatus == '4' or jobstatus == '5' or jobstatus == '8':
                    # job finished, so check for results:
                    status, response = APICall('GET', u'task/%s/result'%taskpk, url_params={'limit':1, 'optimization':'None'})
                    assert(status==200)
                    if len(response['objects']) > 0:
                        # have a response, so return!
                        jobpk = None
                        result = response['objects'][0]
                        if 'errormessage' in result and len(result['errormessage']) > 0:
                            raise BinPickingError(result['errormessage'])
                        
                        return result['output']
                    
            except socket.error, e:
                log.error(e)
                
            # tasks can be long, so sleep
            time.sleep(.1)
            
    finally:
        if jobpk is not None:
            log.info('deleting previous job')
            APICall('DELETE', 'job/%s'%jobpk)

def ExecuteHandEyeCalibrationTaskSync(scenepk, taskparameters):
    '''
    :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
    '''
    taskpk = GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
    # set the task parameters
    APICall('PUT', u'scene/%s/task/%s'%(scenepk, taskpk), data={'tasktype':'handeyecalibration', 'taskparameters':taskparameters})
    # # just in case, delete all previous tasks
    APICall('DELETE', 'job')    
    # execute the task
    status, response = APICall('POST', u'scene/%s/task/%s/result'%(scenepk, taskpk))
    assert(status==200)
    return response

def ExecuteHandEyeCalibrationTaskAsync(scenepk, taskparameters, timeout=1000):
    """
    :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
    """
    taskpk = GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
    # set the task parameters
    APICall('PUT', u'scene/%s/task/%s'%(scenepk, taskpk), data={'tasktype':'handeyecalibration', 'taskparameters':taskparameters})
    # just in case, delete all previous tasks
    APICall('DELETE', 'job')    
    # execute the task
    status, response = APICall('POST', u'scene/%s/task/%s'%(scenepk, taskpk))
    assert(status==200)

    # the jobpk allows us to track the job
    jobpk=response['jobpk']
    # query the task results
    status_text_prev = None
    starttime = time.time()
    try:
        while True:
            try:
                if timeout is not None and time.time()-starttime > timeout:
                    raise TimeoutError('failed to get result in time, quitting')
                
                try:
                    status, response = APICall('GET', u'job/%s'%jobpk)
                    if status == 200:
                        if status_text_prev is not None and status_text_prev != response['status_text']:
                            log.info(response['status_text'])
                        status_text_prev = response['status_text']
                        
                    jobstatus = response['status']
                except APIServerError, e:
                    # most likely job finished
                    log.warn(u'problem with requesting job: %s', e)
                    jobstatus = '2'
                if jobstatus == '2' or jobstatus == '3' or jobstatus == '4' or jobstatus == '5' or jobstatus == '8':
                    # job finished, so check for results:
                    status, response = APICall('GET', u'task/%s/result'%taskpk, url_params={'limit':1, 'optimization':'None'})
                    assert(status==200)
                    if len(response['objects']) > 0:
                        # have a response, so return!
                        jobpk = None
                        result = response['objects'][0]
                        if 'errormessage' in result and len(result['errormessage']) > 0:
                            raise HandEyeCalibrationError(result['errormessage'])
                        
                        return result['output']
                    
            except socket.error, e:
                log.error(e)
                
            # tasks can be long, so sleep
            time.sleep(.1)
            
    finally:
        if jobpk is not None:
            log.info('deleting previous job')
            APICall('DELETE', 'job/%s'%jobpk)
def GetObjects(scenepk):
    """returns all the objects and their translations/rotations
    """
    status, response = APICall('GET', u'scene/%s/instobject'%(scenepk), data={})
    instobjects = {}
    for objvalues in response['instobjects']:
        instobjects[objvalues['name']] = objvalues
    return instobjects

def UpdateObjects(scenepk, objectdata):
    """updates the objects. objectdata is in the same format as returned by GetObjects
    """
    transformtemplate = '{"pk":"%s","quaternion":[%.15f, %.15f, %.15f, %.15f], "translate":[%.15f, %.15f, %.15f] %s}'
    objects = []
    for name, values in objectdata.iteritems():
        objects.append({'pk': values['pk'], 'quaternion':list(values['quaternion']), 'translate':list(values['translate'])})
    status, response = APICall('PUT', u'scene/%s/instobject'%(scenepk), data={'objects':objects})

"""
FIXME
UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 0: ordinal not in range(128) │started densowave bcap zmq server                │www-data@controller3:~$ ~/bin/killslave.bash    

def GetCameraImage(scenepk):
    #image/get/?format=jpeg&width=800&height=600&force=1
    status, response = APICall('GET',u'scene/%s/image/get/?format=jpeg&width=800&height=600&force=1'%(scenepk))
"""

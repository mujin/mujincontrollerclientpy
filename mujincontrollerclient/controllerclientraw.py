# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
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
from urllib import urlencode
from threading import Lock
import re
import time
import logging
import socket
log = logging.getLogger(__name__)

try:
    import simplejson as json
except ImportError:
    import json

from . import APIServerError, FluidPlanningError, BinPickingError, HandEyeCalibrationError, TimeoutError

g_HTTPLock = Lock()

class ControllerWebClient(object):
    _baseControllerUrl = None
    _username = None
    _password = None
    _HTTP = None
    _HTTPHeaders = None
    _HTTPLock = None

    def __init__(self, basecontrollerurl, username, password):
        self._baseControllerUrl = basecontrollerurl
        self._username = username
        self._password = password
        self._HTTPLock = g_HTTPLock#Lock()
        
    def Login(self, timeout=None):
        with self._HTTPLock:
            self._Login(timeout)
            
    def _Login(self, timeout=None):
        csrfpattern = re.compile('csrftoken=(?P<id>[0-9a-zA-Z]*);')
        if httplib2.__version__.startswith('0.7'):
            self._HTTP = Http(".cache", disable_ssl_certificate_validation=True, timeout=timeout)
        else:
            self._HTTP = Http(".cache", timeout=timeout)
            
        #pw = options.pw.replace('\\','')
        self._HTTP.add_credentials(self._username, self._password)
        try:
            responsefirst, contentfirst = self._HTTP.request(self._baseControllerUrl + '/login/', u'GET')
        except httplib2.RedirectLimit:
            # most likely apache2-only authentication and login page isn't needed, however need to send another GET for the csrftoken
            responsefirst, contentfirst = self._HTTP.request(self._baseControllerUrl + '/api/v1/', u'GET')
            sessioncookie = responsefirst.get('set-cookie')
            csrftoken = csrfpattern.findall(sessioncookie)[0]
            self._HTTPHeaders = {'Cookie': sessioncookie}
            if 'location' in responsefirst:
                self._HTTPHeaders['Referer'] = responsefirst['location']
            # the get API CSRF token
            self._HTTPHeaders['X-CSRFToken'] = csrftoken
            self._HTTPHeaders['Content-Type'] = 'application/json; charset=UTF-8'
            if 'location' in responsefirst:
                self._HTTPHeaders['Referer'] = responsefirst['location']
            return
        
        firstcsrftoken = None
        if responsefirst is not None and len(csrfpattern.findall(responsefirst['set-cookie'])) != 0:
            firstcsrftoken = csrfpattern.findall(responsefirst['set-cookie'])[0]
        else:
            responsefirst, contentfirst = self._HTTP.request(self._baseControllerUrl + '/api/v1/', u'GET')
            firstcsrftoken = csrfpattern.findall(responsefirst['set-cookie'])[0]
            
        # login
        self._HTTPHeaders = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': responsefirst['set-cookie']
        }
        #headers['User-agent'] = 'Mozilla/5.0'
        self._HTTPHeaders['Referer'] = self._baseControllerUrl + '/login/'
        loginbody = {
            'username': self._username,
            'csrfmiddlewaretoken': firstcsrftoken,
            'password': self._password,
            'this_is_the_login_form': '1',
            'next': '/'
        }
        
        response, content = self._HTTP.request(self._baseControllerUrl + '/login/', 'POST', headers=self._HTTPHeaders, body=urlencode(loginbody))
        
        if response['status'] != '302' and response['status'] != '200':
            raise ValueError(u'failed to authenticate: %r' % response)
        
        sessioncookie = response.get('set-cookie', responsefirst['set-cookie'])
        
        self._HTTPHeaders = {'Cookie': sessioncookie}
        if 'location' in response:
            self._HTTPHeaders['Referer'] = response['location']
            
        # the get API CSRF token
        response, content = self._HTTP.request(self._baseControllerUrl + '/api/v1/profile', 'GET', headers=self._HTTPHeaders)
        csrftoken = json.loads(content)['csrf_token']
        self._HTTPHeaders['Cookie'] += ';csrftoken=' + csrftoken
        self._HTTPHeaders['X-CSRFToken'] = csrftoken
        self._HTTPHeaders['Content-Type'] = 'application/json; charset=UTF-8'
        if 'location' in response:
            self._HTTPHeaders['Referer'] = response['location']
            
    def RestartPlanningServer(self):
        with self._HTTPLock:
            if self._HTTP is None or self._HTTPHeaders is None:
                self.Login()
            status, response = self._HTTP.request(self._baseControllerUrl + '/restartserver/', 'POST', headers=self._HTTPHeaders)
            assert(status['status'] == 200)
            return json.loads(response)
        
    def IsVerified(self):
        with self._HTTPLock:
            return self._HTTP is not None and self._HTTPHeaders is not None
        
    # python port of the javascript API Call function
    def APICall(self, *args, **kwargs):
        with self._HTTPLock:
            return self._APICall(*args, **kwargs)
        
    def _APICall(self, request_type, api_url, url_params=None, fields=None, data=None):
        if self._HTTP is None or self._HTTPHeaders is None:
            self._Login()
            
        if api_url[-1] != '/':
            api_url += '/'
        url = self._baseControllerUrl + '/api/v1/' + api_url + '?format=json'
        
        if url_params is None:
            url_params = {}
            
        if fields is not None:
            url_params['fields'] = fields
            
        # implicit order by pk
        if 'order_by' not in url_params:
            url_params['order_by'] = 'pk'
            
        for param, value in url_params.iteritems():
            url += '&' + str(param) + '=' + str(value)
            
        if data is None:
            data = {}
            
        request_type = request_type.upper()
        
        log.debug('%s %s', request_type, url)
        response, content = self._HTTP.request(url, request_type, body=json.dumps(data), headers=self._HTTPHeaders)
        
        if request_type == 'DELETE' and response.status == 204:
            # just return without doing anything for deletes
            return response.status, content
        else:
            # try to convert everything else
            error_base = u'\n\nError with %s to %s\n\nThe API call failed (status: %s)' % (request_type, url, response.status)
            try:
                content = json.loads(content)
            except ValueError:
                # either response was empty or not JSON
                raise APIServerError(u'%s, here is what came back in the request:\n%s' % (error_base, unicode(content, 'utf-8')))
            
            if 'traceback' in content:
                raise APIServerError('%s, here is the stack trace that came back in the request:\n%s' % (error_base, unicode(content['traceback'], 'utf-8')))
            else:
                return response.status, content
            
    def GetOrCreateTask(self, *args, **kwargs):
        with self._HTTPLock:
            return self._GetOrCreateTask(*args, **kwargs)
        
    def _GetOrCreateTask(self, scenepk, taskname, tasktype=None):
        """gets or creates a task, returns its pk
        """
        status, response = self._APICall(u'GET', u'scene/%s/task' % scenepk, url_params={'limit': 1, 'name': taskname, 'fields': 'pk,tasktype'})
        assert(status == 200)
        if len(response['objects']) > 0:
            if tasktype is not None:
                assert(response['objects'][0]['tasktype'] == tasktype)
            return response['objects'][0]['pk']
        else:
            status, response = self._APICall(u'POST', u'scene/%s/task' % scenepk, url_params={'fields': 'pk'}, data={"name": taskname, "tasktype": tasktype, "scenepk": scenepk})
            assert(status == 201)
            return response['pk']
        
    def ExecuteFluidTask(self, scenepk, taskparameters, timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        with self._HTTPLock:
            taskpk = self._GetOrCreateTask(scenepk, 'test0', 'fluidplanning')
            # set the task parameters
            self._APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'fluidplanning', 'taskparameters': taskparameters})
            # just in case, delete all previous tasks
            self._APICall('DELETE', 'job')
            # execute the task
            status, response = self._APICall('POST', u'scene/%s/task/%s' % (scenepk, taskpk))
            assert(status == 200)
            # the jobpk allows us to track the job
            jobpk = response['jobpk']
            # query the task results
            status_text_prev = None
            starttime = time.time()
            try:
                while True:
                    try:
                        if timeout is not None and time.time() - starttime > timeout:
                            raise TimeoutError('failed to get result in time, quitting')
                        try:
                            status, response = self._APICall('GET', u'job/%s' % jobpk)
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
                            status, response = self._APICall('GET', u'task/%s/result' % taskpk, url_params={'limit': 1, 'optimization': 'None'})
                            assert(status == 200)
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
                    self._APICall('DELETE', 'job/%s' % jobpk)
                    
    def ExecuteBinPickingTaskSync(self, scenepk, taskparameters, forcecancel=False):
        '''
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: if True, then cancel all previously running jobs before running this one
        '''
        with self._HTTPLock:
            taskpk = self._GetOrCreateTask(scenepk, 'binpickingtask1', 'binpicking')
            # set the task parameters
            self._APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'binpicking', 'taskparameters': taskparameters})
            if forcecancel:
                # # just in case, delete all previous tasks
                self._APICall('DELETE', 'job')
            # execute the task
            status, response = self._APICall('POST', u'scene/%s/task/%s/result' % (scenepk, taskpk))
            assert(status == 200)
            return response
        
    def ExecuteBinPickingTask(self, scenepk, taskparameters, timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        with self._HTTPLock:
            taskpk = self._GetOrCreateTask(scenepk, 'binpickingtask1', 'binpicking')
            # set the task parameters
            self._APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'binpicking', 'taskparameters': taskparameters})
            # just in case, delete all previous tasks
            self._APICall('DELETE', 'job')
            # execute the task
            #status, response = _APICall('POST', u'scene/%s/task/%s'%(scenepk, taskpk))
            status, response = self._APICall('POST', u'job', data={'resource_type': 'task', 'target_pk': taskpk})
            assert(status == 200)
            # the jobpk allows us to track the job
            jobpk = response['jobpk']
            # query the task results
            status_text_prev = None
            starttime = time.time()
            try:
                while True:
                    try:
                        if timeout is not None and time.time() - starttime > timeout:
                            raise TimeoutError('failed to get result in time, quitting')
                        try:
                            status, response = self._APICall('GET', u'job/%s' % jobpk)
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
                            status, response = self._APICall('GET', u'task/%s/result' % taskpk, url_params={'limit': 1, 'optimization': 'None'})
                            assert(status == 200)
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
                    self._APICall('DELETE', 'job/%s' % jobpk)
                    
    def ExecuteHandEyeCalibrationTaskSync(self, scenepk, taskparameters):
        '''
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        '''
        with self._HTTPLock:
            taskpk = self._GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
            # set the task parameters
            self._APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'handeyecalibration', 'taskparameters': taskparameters})
            # # just in case, delete all previous tasks
            self._APICall('DELETE', 'job')
            # execute the task
            status, response = self._APICall('POST', u'scene/%s/task/%s/result' % (scenepk, taskpk))
            assert(status == 200)
            return response
        
    def ExecuteHandEyeCalibrationTaskAsync(self, scenepk, taskparameters, timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        with self._HTTPLock:
            taskpk = self._GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
            # set the task parameters
            self._APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'handeyecalibration', 'taskparameters': taskparameters})
            # just in case, delete all previous tasks
            self._APICall('DELETE', 'job')
            # execute the task
            status, response = self._APICall('POST', u'scene/%s/task/%s' % (scenepk, taskpk))
            assert(status == 200)
            # the jobpk allows us to track the job
            jobpk = response['jobpk']
            # query the task results
            status_text_prev = None
            starttime = time.time()
            try:
                while True:
                    try:
                        if timeout is not None and time.time() - starttime > timeout:
                            raise TimeoutError('failed to get result in time, quitting')
                        try:
                            status, response = self._APICall('GET', u'job/%s' % jobpk)
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
                            status, response = self._APICall('GET', u'task/%s/result' % taskpk, url_params={'limit': 1, 'optimization': 'None'})
                            assert(status == 200)
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
                    self._APICall('DELETE', 'job/%s' % jobpk)

    def GetObjects(self, scenepk):
        """returns all the objects and their translations/rotations
        """
        with self._HTTPLock:
            status, response = self._APICall('GET', u'scene/%s/instobject' % (scenepk), data={})
            instobjects = {}
            for objvalues in response['instobjects']:
                instobjects[objvalues['name']] = objvalues
            return instobjects
        
    def UpdateObjects(self, scenepk, objectdata):
        """updates the objects. objectdata is in the same format as returned by GetObjects
        """
        with self._HTTPLock:
            objects = []
            for name, values in objectdata.iteritems():
                objects.append({'pk': values['pk'], 'quaternion': list(values['quaternion']), 'translate': list(values['translate'])})
            status, response = self._APICall('PUT', u'scene/%s/instobject' % (scenepk), data={'objects': objects})
            return response

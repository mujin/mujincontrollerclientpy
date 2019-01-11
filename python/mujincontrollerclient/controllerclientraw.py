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
import os
import requests
import requests.auth

from . import GetAPIServerErrorFromWeb
from . import json

import logging
log = logging.getLogger(__name__)

class ControllerWebClient(object):
    _baseurl = None # base url of the controller
    _username = None # username to login with
    _password = None # password to login with
    _headers = None # prepared headers for all requests
    _isok = False # flag to stop
    _session = None # requests session object

    def __init__(self, baseurl, username, password, locale=None):
        self._baseurl = baseurl
        self._username = username
        self._password = password
        self._headers = {}
        self._isok = True

        # any string can be the csrftoken
        self._headers['X-CSRFToken'] = 'csrftoken'

        self._session = requests.Session()
        self._session.auth = requests.auth.HTTPBasicAuth(self._username, self._password)
        self._session.cookies.set('csrftoken', self._headers['X-CSRFToken'], path='/')

        self.SetLocale(locale)

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()

    def SetDestroy(self):
        self._isok = False

    def SetLocale(self, locale=None):
        locale = locale or os.environ.get('LANG', None)

        # convert locale to language code for http requests
        # en_US.UTF-8 => en-us
        # en_US => en-us
        # en => en
        language = 'en' # default to en
        if locale is not None and len(locale) > 0:
            language = locale.split('.', 1)[0].replace('_', '-').lower()
        self._headers['Accept-Language'] = language

    def Request(self, method, path, timeout=5, headers=None, **kwargs):
        url = self._baseurl + path

        # set all the headers prepared for this client
        headers = dict(headers or {})
        headers.update(self._headers)

        # for GET and HEAD requests, have a retry logic in case keep alive connection is being closed by server
        if method in ('GET', 'HEAD'):
            try:
                return self._session.request(method=method, url=url, timeout=timeout, headers=headers, **kwargs)
            except requests.ConnectionError as e:
                log.warn('caught connection error, maybe server is racing to close keep alive connection, try again: %s', e)
        return self._session.request(method=method, url=url, timeout=timeout, headers=headers, **kwargs)

    # python port of the javascript API Call function
    def APICall(self, request_type, api_url='', url_params=None, fields=None, data=None, headers=None, timeout=5):
        path = '/api/v1/' + api_url.lstrip('/')
        if not path.endswith('/'):
            path += '/'

        if url_params is None:
            url_params = {}

        url_params['format'] = 'json'

        if fields is not None:
            url_params['fields'] = fields

        # implicit order by pk
        if 'order_by' not in url_params:
            url_params['order_by'] = 'pk'

        if data is None:
            data = {}

        if headers is None:
            headers = {}

        # default to json content type
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(data)

        request_type = request_type.upper()

        log.verbose('%s %s', request_type, self._baseurl + path)
        response = self.Request(request_type, path, params=url_params, data=data, headers=headers, timeout=timeout)

        if request_type == 'HEAD' and response.status_code == 200:
            # just return without doing anything for head
            return response.status_code, response.content

        if request_type == 'DELETE' and response.status_code == 204:
            # just return without doing anything for deletes
            return response.status_code, response.content

        # try to convert everything else
        try:
            content = json.loads(response.content)
        except ValueError as e:
            log.warn(u'caught exception during json decode for content (%r): %s', response.content.decode('utf-8'), e)
            raise GetAPIServerErrorFromWeb(request_type, self._baseurl + path, response.status_code, response.content)
        
        if 'stacktrace' in content or response.status_code >= 400:
            raise GetAPIServerErrorFromWeb(request_type, self._baseurl + path, response.status_code, response.content)
        
        return response.status_code, content

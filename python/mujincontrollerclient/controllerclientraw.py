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
import time

import logging
log = logging.getLogger(__name__)

try:
    import ujson as json
except ImportError:
    import json

from . import ControllerClientError
from . import APIServerError, AuthenticationError, GetAPIServerErrorFromWeb
from . import ugettext as _

class ControllerWebClient(object):
    _baseurl = None
    _username = None
    _password = None
    _session = None
    _csrftoken = None
    _locale = None
    _language = None
    _isok = False

    def __init__(self, baseurl, username, password, locale=None):
        self._baseurl = baseurl
        self._username = username
        self._password = password
        self._session = None
        self._csrftoken = None
        self._locale = None
        self._language = None

        self._isok = True
        self.SetLocale(locale)

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()
        self.Logout()

    def SetDestroy(self):
        self._isok = False

    def SetLocale(self, locale=None):
        self._locale = locale or os.environ.get('LANG', None)

        # convert locale to language code for http requests
        # en_US.UTF-8 => en-us
        # en_US => en-us
        # en => en
        self._language = 'en' # default to en
        if self._locale is not None and len(self._locale) > 0:
            self._language = self._locale.split('.', 1)[0].replace('_', '-').lower()

    def Login(self, timeout=5):
        if self._session is not None:
            return

        session = requests.Session()
        session.auth = requests.auth.HTTPBasicAuth(self._username, self._password)

        headers = {
            'Accept-Language': self._language,
        }
        response = session.get('%s/login/' % self._baseurl, headers=headers, timeout=timeout)
        if response.status_code != requests.codes.ok:
            raise AuthenticationError(_('Failed to authenticate: %r') % response.content)

        csrftoken = response.cookies.get('csrftoken', None)

        data = {
            'username': self._username,
            'password': self._password,
            'this_is_the_login_form': '1',
            'next': '/',
        }

        headers = {
            'X-CSRFToken': csrftoken,
            'Accept-Language': self._language,
        }
        response = session.post('%s/login/' % self._baseurl, data=data, headers=headers, timeout=timeout)

        if response.status_code != requests.codes.ok:
            raise AuthenticationError(_('Failed to authenticate: %r') % response.content)

        self._session = session
        self._csrftoken = csrftoken

    def Logout(self):
        self._csrftoken = None
        if self._session is not None:
            self._session.close()
            self._session = None

    def IsLoggedIn(self):
        return self._session is not None

    def Request(self, method, path, timeout=5, headers=None, **kwargs):
        if not self.IsLoggedIn():
            self.Login(timeout=timeout)

        url = self._baseurl + path

        if headers is None:
            headers = {}

        headers['Accept-Language'] = self._language
        if self._csrftoken:
            headers['X-CSRFToken'] = self._csrftoken

        return self._session.request(method=method, url=url, timeout=timeout, headers=headers, **kwargs)
	
    # python port of the javascript API Call function
    def APICall(self, request_type, api_url, url_params=None, fields=None, data=None, timeout=5):

        if not api_url.endswith('/'):
            api_url += '/'
        path = '/api/v1/' + api_url

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

        request_type = request_type.upper()

        log.verbose('%s %s', request_type, self._baseurl + path)
        response = self.Request(request_type, path, params=url_params, data=json.dumps(data), timeout=timeout)

        if request_type == 'DELETE' and response.status_code == 204:
            # just return without doing anything for deletes
            return response.status_code, response.content

        # try to convert everything else
        try:
            content = json.loads(response.content)
        except ValueError:
            self.Logout() # always logout the session when we hit an error
            raise GetAPIServerErrorFromWeb(request_type, self._baseurl + path, response.status_code, response.content)
        
        if 'stacktrace' in content or response.status_code >= 400:
            self.Logout() # always logout the session when we hit an error
            raise GetAPIServerErrorFromWeb(request_type, self._baseurl + path, response.status_code, response.content)
        
        return response.status_code, content

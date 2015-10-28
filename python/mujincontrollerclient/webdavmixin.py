# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.

import datetime

class WebDAVMixin:

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

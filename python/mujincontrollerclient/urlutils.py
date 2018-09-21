# -*- coding: utf-8 -*-
# Copyright (C) 2018 MUJIN Inc

# this file contains conversion functions between the following things:
# - URI (mujin:/somefolder/somefile.mujin.dae) (utf8/unicode+special urlquoted) (could have fragment) (file://abc/xxx.mujin.dae#body0_motion)
# - PrimaryKey (somefolder%2Fsomefile.mujin.dae) (ascii+urlquoted) (could have fragment) (mitsubishi%2Fmitsubishi-rv-7f.mujin.dae%40body0_motion) (enforce return type to be str)
# - Filename (somefolder/somefile.mujin.dae) (utf8/unicode) (should not have fragment)
# - PartType (somefolder/somefile) (utf8/unicode) (should not have fragment)
# all public functions in this file should be in the form of Get*From*, take fragementseparator as keyword argument as necessary, take allowfragment as necessary
# all other functions should be internal to this file, prefixed with _

# the outside world uses this specifier to signify a '#' specifier. This is needed
# because '#' in URL parsing is a special role
from urlparse import urlparse, urlunparse, ParseResult
import urllib
import os
import logging
from mujincommon import MujinExceptionBase

log = logging.getLogger(__name__)

def _ParseURI(uri, allowfragments=True, fragmentseparator='@'):
    u""" Mujin uri is unicode and special characters like #, ? and @ will be part of the path

    uri will include 5 parts <scheme>://<netloc>/<path>?<query>#<fragment>
    mujinuri only have scheme which is mujin:/ , other scheme will use standard python library to parse.
    mujinuri will not have # as fragment part because we use @ as separator to separate lie abc.mujin.dae@body0_motion
    
    >>> print(_ParseURI(u"mujin:/测试_test.mujin.dae", allowfragments=True, fragmentseparator='@').path)
    /测试_test.mujin.dae
    >>> _ParseURI(u"mujin:/测试_test.mujin.dae@body0_motion", allowfragments=False, fragmentseparator='@').fragment
    ''
    >>> print(_ParseURI(u"mujin:/测试_test.mujin.dae@body0_motion", allowfragments=True, fragmentseparator='#').path)
    /测试_test.mujin.dae@body0_motion
    """
    uri = unicode(uri)
    i = uri.find(':')
    if not uri[:i].lower() == "mujin":
        # if scheme is not mujin specified, use the standard uri parse
        return urlparse(uri, allowfragments)
    else:
        # it's a mujinuri
        scheme = uri[:i].lower()
        uri = uri[i+1:]
        if uri[:2] == "//":
            # usually we need to split hostname from url
            # for now mujin uri doesn't have definition of hostname in uri
            log.warn("uri {} includs hostname which is not defined".format(uri))
            raise MujinExceptionBase('mujin scheme has no hostname defined %s'%uri)
        else:
            if allowfragments:
                # split by the last appeared fragmentseparator
                separatorindex = uri.rfind(fragmentseparator)
                if separatorindex >= 0:
                    path = uri[:separatorindex]
                    fragment = uri[separatorindex+1:]
                else:
                    path = uri
                    fragment = ""
            else:
                path = uri
                fragment = ""
            parseresult = ParseResult(scheme, "", path, params="", query="", fragment=fragment)
    return parseresult

def _UnparseURI(uriparts, fragmentseparator):
    u""" compose a uri. This function will call urlunparse if scheme is not mujin.

    uriparts is a ParseResult or a tuple which has six parts (scheme, netloc, path, params, query, fragment)

    >>> print(_UnparseURI(('mujin', '', u'测试_test.mujin.dae', '', '', 'body0_motion'), fragmentseparator='@'))
    mujin:/\u6d4b\u8bd5_test.mujin.dae@body0_motion
    """
    scheme, netloc, url, params, query, fragment = uriparts
    if scheme == "mujin":
        assert netloc == ""
        assert params == ""
        assert query == ""
        if url and url[:1] != '/':
            url = '/' + url
        if fragment:
            url = url + fragmentseparator + fragment
        return unicode(scheme + ':' + url)
    else:
        # for rfc urlparse, make sure fragment_separator is #
        if fragment != '#':
            log.warn("_UnparseURI get wrong fragment separator {} with scheme {}".format(fragmentseparator, scheme))
        return unicode(urlunparse((scheme, netloc, url, params, query, fragment)))

def GetSchemeFromURI(uri):
    u"""
    >>> GetSchemeFromURI("mujin:/test.mujin.dae")
    u'mujin'
    >>> GetSchemeFromURI("file:/test.mujin.dae")
    u'file'
    """
    return _ParseURI(uri).scheme

def GetFragmentFromURI(uri, fragmentseparator):
    u"""
    >>> GetFragmentFromURI(u"mujin:/测试_test.mujin.dae", fragmentseparator='@')
    ''
    >>> GetFragmentFromURI(u"mujin:/测试_test.mujin.dae@body0_motion", fragmentseparator='@')
    u'body0_motion'
    >>> GetFragmentFromURI(u"mujin:/测试_test.mujin.dae#body0_motion", fragmentseparator='@')
    ''
    """
    return _ParseURI(uri, fragmentseparator).fragment

def GetPrimaryKeyFromURI(uri, allowfragments, fragmentseparator, primarykeyseparator):
    u"""
    uri is a mujin scheme uri which is unicode
    primarykey is utf-8 encoded and quoted.
    example:

    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='@', primarykeyseparator='@')
    '%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion'
    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='@', primarykeyseparator='#')
    '%E6%B5%8B%E8%AF%95_test..mujin.dae#body0_motion'
    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='#', primarykeyseparator='@')
    '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'
    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='#', primarykeyseparator='#')
    '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'
    """
    res = _ParseURI(uri, allowfragments=allowfragments, fragmentseparator=fragmentseparator)
    if res.fragment:
        return str(urllib.quote(res.path[1:].encode('utf-8'))+ str(primarykeyseparator) + urllib.quote(res.fragment.encode('utf-8')))
    else:
        return str(urllib.quote(res.path[1:].encode('utf-8')))


def GetPrimaryKeyFromFilename(filename, mujinpath):
    """  extract primarykey from filename . 

    filename is unicode without quote. need to remove mujinpath if it's given.

    >>> GetPrimaryKeyFromFilename("/data/detection/测试_test.mujin.dae", "/data/detection")
    '%E6%B5%8B%E8%AF%95_test.mujin.dae'
    >>> GetPrimaryKeyFromFilename("/data/u/mujin/测试_test.mujin.dae", "/data/detection")
    '/data/u/mujin/%E6%B5%8B%E8%AF%95_test.mujin.dae'
    """
    if mujinpath and filename.startswith(mujinpath):
        filename = filename[len(mujinpath)+1:]
    return urllib.quote(filename.encode('utf-8'))

def GetURIFromURI(uri, allowfragments, fragmentseparator, keepfragment=False, newfragmentseparator=''):
    """ Compose a new uri from old one
    allowfragments: if it's true, ParseURI will keep the fragments of old uri
    fragmentseparator: the separator used in old uri
    keepfragment: uri fragment part will be kept in the new uri if Ture, otherwise it will be removed.
    newfragmentseparator:  the new fragment separator used in new uri.

    >>> GetURIFromURI(u"mujin:/test.mujin.dae@body0_motion", allowfragments=True, fragmentseparator='@', keepfragment=True, newfragmentseparator='#')
    u'mujin:/test.mujin.dae#body0_motion'
    >>> GetURIFromURI(u"mujin:/test.mujin.dae@body0_motion", allowfragments=True, fragmentseparator='@', keepfragment=False, newfragmentseparator='#')
    u'mujin:/test.mujin.dae'
    """
    res = _ParseURI(uri, allowfragments=allowfragments, fragmentseparator=fragmentseparator)
    if not newfragmentseparator:
        newfragmentseparator = fragmentseparator
    if keepfragment:
        uri = _UnparseURI((res.scheme, res.netloc, res.path, res.params, res.query, res.fragment), fragmentseparator=newfragmentseparator)
    else:
        uri = _UnparseURI((res.scheme, res.netloc, res.path, res.params, res.query, ""), fragmentseparator=newfragmentseparator) # remove the fragment part
    return uri

def GetURIFromPrimaryKey(pk, primarykeyseparator, fragmentseparator):
    """Given the encoded primary key (utf-8 encoded and quoted), returns the unicode URL.

    >>> print(GetURIFromPrimaryKey('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', primarykeyseparator='@', fragmentseparator='#'))
    mujin:/测试_test..mujin.dae#body0_motion
    """
    pk = str(pk)
    unicodepk = urllib.unquote(pk).decode('utf-8')
    index = unicodepk.rfind(primarykeyseparator)
    if index >= 0:
        path = unicodepk[:index]
        fragment = unicodepk[index+1:]
    else:
        path = unicodepk
        fragment = ""
    return _UnparseURI(('mujin', '', path, '', '', fragment), fragmentseparator)


def GetURIFromFilename(filename, mujinpath):
    """ Compose a mujin uri from filename.

    >>> GetURIFromFilename(u"/data/detection/test.mujin.dae", u"/data/detection")
    u'mujin:/test.mujin.dae'
    """
    filename = filename[len(mujinpath)+1:]
    return _UnparseURI(('mujin', '', filename , '', '', ''), '') # no fragment


def GetFilenameFromPrimaryKey(pk, primarykeyseparator):
    u""" return filename from primary key

    >>> print(GetFilenameFromPrimaryKey('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', '@'))
    测试_test..mujin.dae
    """
    pk = str(pk)
    uri = GetURIFromPrimaryKey(pk, primarykeyseparator, '#') # here uri fragment separator is not important , since our goal is to remove fragment here.
    baseuri = GetURIFromURI(uri, allowfragments=True, fragmentseparator='#')
    parseduri = _ParseURI(baseuri, allowfragments=False)
    filename = parseduri.path[1:] # the first character is /
    return unicode(filename)

def GetFilenameFromURI(uri, mujinpath, allowfragments=True, fragmentseparator='@'):
    u"""returns the filesystem path that the URI points to.

    uri: if uri is mujin scheme, will join mujin path. otherwise it will directly use parsed path result.

    >>> print(GetFilenameFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae',u'/var/www/media/u/testuser')[1])
    /var/www/media/u/testuser/検証動作1_121122.mujin.dae
    """
    res = _ParseURI(uri, allowfragments=allowfragments, fragmentseparator=fragmentseparator)
    if len(res.path) == 0:
        raise MujinExceptionBase('need path in URI %s'% uri)

    if res.scheme == "mujin":
        filepath = os.path.join(mujinpath, res.path[1:])
    else:
        filepath = res.path
    return res, unicode(filepath)

def GetFilenameFromPartType(parttype, suffix='.mujin.dae'):
    u""" Unquote parttype to get filename, if withsuffix is True, add the .mujin.dae suffix

    >>> print(GetFilenameFromPartType(u'测试_test', suffix='.tar.gz'))
    测试_test.tar.gz
    """
    if suffix:
        return unicode(parttype +  suffix)
    else:
        return unicode(parttype)   # used to compose filename.tar.gz

def GetPartTypeFromPrimaryKey(pk):
    u""" return a unicode partype

    >>> print(GetPartTypeFromPrimaryKey('%E6%B5%8B%E8%AF%95_test.mujin.dae'))
    测试_test
    """
    pk = str(pk)
    if pk.endswith('.mujin.dae'):
        return urllib.unquote(pk[:-len(".mujin.dae")]).decode('utf-8')
    else:
        return urllib.unquote(pk).decode('utf-8')

def GetPrimaryKeyFromPartType(parttype):
    u"""
    >>> GetPrimaryKeyFromPartType(u'测试_test')
    '%E6%B5%8B%E8%AF%95_test.mujin.dae'
    """
    return str(urllib.quote( (parttype+".mujin.dae").encode('utf-8')))

def GetPartTypeFromFilename(filename, mujinpath="", suffix=".mujin.dae"):
    u"""
    >>> print(GetPartTypeFromFilename(u"/data/detection/测试_test.mujin.dae", mujinpath="/data/detection", suffix=".mujin.dae"))
    测试_test
    """
    if mujinpath and filename.startswith(mujinpath):
        filename = filename[len(mujinpath)+1:]
    if filename.endswith(suffix):
        filename = filename[:-len(suffix)]
    return unicode(filename)
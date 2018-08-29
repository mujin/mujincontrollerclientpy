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

id_separator = u'@'
fragment_separator = u'#'


# TODO(simon): make this internal to this file
def ParseMujinURI(uri, allowfragments=True, fragmentidentifier=id_separator):
    """ Mujin uri is unicode and special characters like #, ? and @ will be part of the path

    uri will include 5 parts <scheme>://<netloc>/<path>?<query>#<fragment>
    mujinuri only have scheme which is mujin:/
    mujinuri will not have # as fragment part because we use @ as separator to separate lie abc.mujin.dae@body0_motion
    """

    uri = unicode(uri)
    i = uri.find(':')

    if not uri[:i] == "mujin":
        # if scheme is not mujin specified, use the standard uri parse
        parseresult =  urlparse(uri, allowfragments)
        parseresult = ParseResult(parseresult.scheme, parseresult.netloc, urllib.unquote(parseresult.path), parseresult.params, parseresult.query, parseresult.fragment)
    else:
        # it's a mujinuri
        scheme = uri[:i].lower()
        uri = uri[i+1:]
        if uri[:2] == "//":
            # usually we need to split hostname from url
            # for now mujin uri doesn't have definition of hostname in uri
            log.warn("uri {} includs hostname which is not defined".format(uri))
            raise MujinExceptionBase(_('mujin scheme has no hostname defined {}').format(uri))
        else:
            if allowfragments:
                # split by the last appeared id_separator
                separatorindex = uri.rfind(fragmentidentifier)
                if separatorindex >= 0:
                    path = uri[:separatorindex]
                    fragment = uri[separatorindex+1:]
                else:
                    path = uri
                    fragment = u""
            else:
                path = uri
                fragment = u""
            parseresult = ParseResult(scheme, "", path, params="", query="", fragment=fragment)
    return parseresult


# TODO(simon): make this internal to this file
def UnparseMujinURI(uriparts, fragmentidentifier=id_separator):
    """ compose a uri. This function will call urlunparse if scheme is not mujin.

    uriparts is a ParseResult or a tuple which has six parts (scheme, netloc, path, params, query, fragment)
    """
    scheme, netloc, url, params, query, fragment = uriparts
    if scheme == "mujin":
        assert netloc == ""
        assert params == ""
        assert query == ""
        if url and url[:1] != '/':
            url = '/' + url
        if fragment:
            url = url + fragmentidentifier + fragment
        return unicode( scheme+ ':' + unicode(url) )
    else:
        # for rfc urlparse, make sure fragment_separator is #
        return urlunparse((scheme, netloc, url, params, query, fragment))


def GetPrimaryKeyFromURI(uri):
    """
    uri is a mujin scheme uri which is unicode
    primarykey is utf-8 encoded and quoted.
    example:

      GetPrimaryKeyFromURI(u'mujin:/测试_test_#?._%20_\x03test..mujin.dae')
      returns '%E6%B5%8B%E8%AF%95_test_%23%3F._%2520_%03test..mujin.dae'
    """
    res = ParseMujinURI(uri)
    if res.fragment:
        return urllib.quote(res.path[1:].encode('utf-8'))+ str(id_separator) + urllib.quote(res.fragment.encode('utf-8'))
    else:
        return  urllib.quote(str(res.path[1:]))


def GetPrimaryKeyFromFilename(filename, mujinpath):
    """  extract primarykey from filename . 

    filename is unicode without quote. need to remove mujinpath if it's given.

    >>> GetPrimaryKeyFromFilename("/data/detection/测试_test.mujin.dae", "/data/detection")
    ...%E6%B5%8B%E8%AF%95_test.mujin.dae
    """
    if mujinpath and filename.startswith(mujinpath):
        filename = filename[len(mujinpath)+1:]
    return urllib.quote(filename.encode('utf-8'))

# TODO(simon): make this internal to this file
def GetPrimaryKeyFromParsedURI(res):
    """input the parameters from urlparse

    res: urlparse.ParsedResult
    example:
    GetPrimaryKeyFromURI(urlparse(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae'))
    returns u'%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122.mujin.dae'
    """
    if res.fragment:
        return GetPrimaryKeyFromUnicode(res.path[1:]) + id_separator + GetPrimaryKeyFromUnicode(res.fragment)
    else:
        return GetPrimaryKeyFromUnicode(res.path[1:])

# TODO(simon): need to replace this with FromFilename
def GetPrimaryKeyFromUnicode(s):
    """ Transfer  Unicode str to PrimaryKey(utf-8 encoded and quoted)
    example:

      GetPrimaryKeyFromUnicode(u'\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
      returns: '%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122.mujin.dae'
    """
    return urllib.quote(s.encode('utf-8'))

# TODO(simon): rename this to GetURIFromURI(allowfragment=False, fragmentseparator='#')
# TODO(simon): equivalent to GetURIFromPrimaryKey(GetPrimaryKeyFromURI(uri))
def GetBaseUri(uri):
    """returns the URI before the separator
    """
    res = ParseMujinURI(uri)
    uri = UnparseMujinURI((res.scheme, res.netloc, res.path[1:], res.params, res.query, "")) # remove the fragment part
    return uri

def GetURIFromPrimaryKey(pk):
    """Given the encoded primary key (utf-8 encoded and quoted), returns the unicode URL.
    example:
      GetURIFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122.mujin.dae')
      returns: u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae'
    """
    unicodepk = GetUnicodeFromPrimaryKey(pk)
    index = unicodepk.rfind(id_separator)
    if index >= 0:
        path = unicodepk[:index]
        fragment = unicodepk[index+1:]
    else:
        path = unicodepk
        fragment = ""
    return UnparseMujinURI(('mujin', '', path, '', '', fragment))


def GetURIFromFilename(filename, mujinpath):
    """ Compose a mujin uri from filename. 
    """
    filename = filename[len(mujinpath)+1:]
    return UnparseMujinURI(('mujin', '', filename , '', '', ''))


def GetFilenameFromPrimaryKey(pk):
    """ return filename from primary key
    """
    uri = GetURIFromPrimaryKey(pk)
    parseresult = ParseMujinURI(uri, allowfragments=True) # allow fragments will separate object_pk in fragments
    filename = parseresult.path[1:] # the first character is /
    return filename

def GetFilenameFromURI(uri, mujinpath, allowfragment=True, fragmentidentifier=id_separator):
    """returns the filesystem path that the URI points to.

    uri: if uri is mujin scheme, will join mujin path. otherwise it will directly use parsed path result.
    
    example:
    
      GetFilenameFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae',u'/var/www/media/u/testuser')
      returns: (ParseResult(scheme=u'mujin', netloc='', path=u'/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae', params='', query='', fragment=''), u'/var/www/media/u/testuser/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
    """
    res = ParseMujinURI(uri, allowfragment, fragmentidentifier)
    if len(res.path) == 0:
        raise MujinExceptionBase(_('need path in URI %s') % uri)

    if res.scheme == "mujin":
        filepath = os.path.join(mujinpath, res.path[1:])
    else:
        filepath = res.path
    return res, filepath

# TODO(simon): there is no TargetName there is only PartType
def GetFilenameFromTargetName(targetname, withsuffix=True):
    """ Unquote targetname to get filename, if withsuffix is True, add the .mujin.dae suffix
    """
    filename = urllib.unquote(targetname)
    if withsuffix:
        return filename + ".mujin.dae"
    else:
        return filename   # used to compose filename.tar.gz

# TODO(simon): need to replace this with GetFileName
def GetUnicodeFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode string.
    If pk is a unicode object, will return the string as is.
    
    example:

      GetUnicodeFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122.mujin.dae')
      returns: u'\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae'
    """
    pk = urllib.unquote(pk)
    return pk.decode('utf-8')

# TODO(simon): there is no TargetName there is only PartType
# TODO(simon): PrimaryKey
def GetTargetNameFromPK(pk):
    return pk[:-len(".mujin.dae")]
    
# TODO(simon): there is no TargetName there is only PartType
# TODO(simon): PrimaryKey
def GetPKFromTargetName(name):
    return name+".mujin.dae"

# TODO(simon): there is no TargetName there is only PartType
def GetTargetNameFromFilename(filename, mujinpath=""):
    return GetTargetNameFromPK(GetPrimaryKeyFromFilename(filename, ""))

# TODO(simon): this has to be internal
def Quote(value):
    return urllib.quote(value)

# TODO(simon): this has to be internal
def Unquote(value):
    return urllib.unquote(value)

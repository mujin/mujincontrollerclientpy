#encoding=utf-8

# the outside world uses this specifier to signify a '#' specifier. This is needed
# because '#' in URL parsing is a special role
from urlparse import urlparse, urlunparse, ParseResult
import urllib
import os

id_separator = u'@'
fragment_separator = u'#'



def ParseMujinURI(uri, allowfragments=True, fragmentidentifier=id_separator):
    """ Mujin uri is unicode and special characters like #, ? and @ will be part of the path

    uri will include 5 parts <scheme>://<netloc>/<path>?<query>#<fragment>
    mujinuri only have scheme which is mujin:/
    mujinuri will not have # because we use @ as separator to separate lie abc.mujin.dae@body0_motion
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



def UnparseMujinURI(uriparts, fragmentidentifier=id_separator):
    """ compose a mujin uri
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
    uri is unicode
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


def GetPkFromUrl(username, url, scenetype=None):
    '''
    examples:

      GetPkFromUrl(u'testuser',u'http://localhost/su/testuser/%E3%83%AC%E3%82%A4%E3%82%A2%E3%82%A6%E3%83%88%E8%A9%95%E4%BE%A11_copy.mujin.dae')
      returns: '%E3%83%AC%E3%82%A4%E3%82%A2%E3%82%A6%E3%83%88%E8%A9%95%E4%BE%A11_copy'
    '''
    pk = url[len(u'%(baseurl)s/su/%(username)s/' % {'baseurl': GetBaseUrl(), 'username': username}):]
    # if scenetype is None or scenetype == 'mujincollada':
    #     pk = pk[:pk.find('.mujin.dae')]
    return pk

def GetPrimaryKeyFromFilename(filename, mujinpath):
    return urllib.quote(filename[len(mujinpath)+1:].encode('utf-8'))


def GetPrimaryKeyFromParsedURI(res):
    """input the parameters from urlparse
    example:
    
    GetPrimaryKeyFromURI(urlparse(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae'))
    returns u'%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122'
    """
    if res.fragment:
        return GetPrimaryKeyFromUnicode(res.path[1:]) + id_separator + GetPrimaryKeyFromUnicode(res.fragment)
    else:
        return GetPrimaryKeyFromUnicode(res.path[1:])

def GetPrimaryKeyFromUnicode(s):
    """
    example:

      GetPrimaryKeyFromUnicode(u'\u691c\u8a3c\u52d5\u4f5c1_121122')
      returns: '%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122'
    """
    return urllib.quote(s.encode('utf-8'))


def GetBaseHost():
    MUJIN_DOMAIN_URL = os.environ.get('MUJIN_DOMAIN_URL', None)
    if MUJIN_DOMAIN_URL is not None:
        return unicode(MUJIN_DOMAIN_URL)
    if os.environ.get('MUJIN_ENV', '') == 'production':
        return u'controller.mujin.co.jp'
    else:
        return u'localhost'


def GetBaseUrl():
#    if os.environ.get('MUJIN_ENV','') == 'dev':
#        return u'http://localhost:8000'
    MUJIN_DOMAIN_URL = os.environ.get('MUJIN_DOMAIN_URL', None)
    if MUJIN_DOMAIN_URL is not None:
        return u'https://%s' % MUJIN_DOMAIN_URL

    if os.environ.get('MUJIN_ENV', '') == 'production':
        return u'https://controller.mujin.co.jp'

    else:
        return u'http://localhost'

def GetBaseUri(uri):
    """returns the URI before the separator
    """
    res = ParseMujinURI(uri)
    uri = UnparseMujinURI((res.scheme, res.netloc, res.path[1:], res.params, res.query, "")) # remove the fragment part
    return uri

def GetURIFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode URL.
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



def GetUriFromUrl(username, url, scenetype=None):
    '''
    examples:

      GetUriFromUrl(u'testuser', u'http://localhost/su/testuser/kawada_nut.mujin.dae')
      returns: u'mujin:/kawada_nut.mujin.dae'

      GetUriFromUrl(u'testuser',u'http://localhost/su/testuser/%E3%83%AC%E3%82%A4%E3%82%A2%E3%82%A6%E3%83%88%E8%A9%95%E4%BE%A11_copy.mujin.dae')
      returns: u'mujin:/\u30ec\u30a4\u30a2\u30a6\u30c8\u8a55\u4fa11_copy.mujin.dae'

    '''
    pk = GetPkFromUrl(username, url, scenetype)
    return GetURIFromPrimaryKey(pk)


def GetURIFromFilename(filename, mujinpath):
    filename = filename[len(mujinpath)+1:]
    return UnparseMujinURI(('mujin', '', filename , '', '', ''))

def GetUrlFromPk(username, pk):
    '''
    examples:

      GetUrlFromPk(u'testuser','%E3%83%AC%E3%82%A4%E3%82%A2%E3%82%A6%E3%83%88%E8%A9%95%E4%BE%A11_copy')
      returns: u'http://localhost/su/testuser/%E3%83%AC%E3%82%A4%E3%82%A2%E3%82%A6%E3%83%88%E8%A9%95%E4%BE%A11_copy.mujin.dae'
    '''

    url =  '%(baseurl)s/su/%(username)s/%(pk)s' % {'baseurl': GetBaseUrl(), 'username': username, 'pk': pk}
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    return url

def GetUrlFromUri(username, uri):
    '''
    url includes quote(encoded(uri)) , quote(encoded(uri)) is equal to primarykey
    examples:

      GetUrlFromUri(u'testuser', u'mujin:/kawada_nut.mujin.dae')
      returns: u'http://localhost/su/testuser/kawada_nut.mujin.dae'

      GetUrlFromUri(u'testuser', u'mujin:/wafersupply_d27.mujin.dae@body1_motion')
      returns: u'http://localhost/su/testuser/wafersupply_d27.mujin.dae'

      GetUrlFromUri(u'testuser',u'mujin:/\u30ec\u30a4\u30a2\u30a6\u30c8\u8a55\u4fa11_copy.mujin.dae')
      returns: u'http://localhost/su/testuser/%E3%83%AC%E3%82%A4%E3%82%A2%E3%82%A6%E3%83%88%E8%A9%95%E4%BE%A11_copy.mujin.dae'
    '''
    pk = GetPrimaryKeyFromURI(uri)
    return GetUrlFromPk(username, pk)



def GetFilenameFromPrimaryKey(pk):
    uri = GetURIFromPrimaryKey(pk)
    parseresult = ParseMujinURI(uri, allowfragments=True) # allow fragments will separate object_pk in fragments

    # separatorIndex = pk.find(id_separator)
    # if separatorIndex >= 0:
    #     pk = pk[:separatorIndex]
    # if separatorIndex == 0:
    #     log.warn("GetFilenameFromPrimaryKey, pk start with id_separator")
    # filename = urllib.unquote(pk).decode('utf-8')
    filename = parseresult.path[1:] # the first character is /
    return filename



def GetFilenameFromURI(uri, mujinpath, allowfragment=True, fragmentidentifier=id_separator):
    """returns the filesystem path that the URI points to.
    :param uri: points to mujin:/ resource
    
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

def GetUnicodeFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode string.
    If pk is a unicode object, will return the string as is.
    
    example:

      GetUnicodeFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122')
      returns: u'\u691c\u8a3c\u52d5\u4f5c1_121122'
    """

    pk = urllib.unquote(pk)
    return pk.decode('utf-8')
    # if not isinstance(pk, unicode):
    #     return unicode(unquote(str(pk)), 'utf-8')
    # else:
    #     return pk


def GetTargetNameFromPK(self, pk):
    return urllib.unquote(pk).decode('utf-8')[:-len(".mujin.dae")]

def GetPKFromTargetName(self, name):
    return urllib.quote(name.encode('utf-8')) + ".mujin.dae"

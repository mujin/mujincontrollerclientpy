# -*- coding: utf-8 -*-
# Copyright (C) 2018 MUJIN Inc

"""
this file contains conversion functions between the following things:
- URI (mujin:/somefolder/somefile.mujin.dae) (utf8/unicode+special urlquoted) (could have fragment) (file://abc/xxx.mujin.dae#body0_motion)
- PrimaryKey (somefolder%2Fsomefile.mujin.dae) (ascii+urlquoted) (could have fragment) (mitsubishi%2Fmitsubishi-rv-7f.mujin.dae@body0_motion) (enforce return type to be str)
- Filename (somefolder/somefile.mujin.dae) (utf8/unicode) (should not have fragment)
- PartType (somefolder/somefile) (utf8/unicode) (should not have fragment)
all public functions in this file should be in the form of Get*From*, take fragementseparator as keyword argument as necessary, take allowfragment as necessary
# all other functions should be internal to this file, prefixed with _

the outside world uses this specifier to signify a FRAGMENT_SEPARATOR_SHARP specifier. This is needed
because FRAGMENT_SEPARATOR_SHARP in URL parsing is a special role
"""

try:
    from urllib.parse import quote, unquote
except ImportError:
    from urllib import quote, unquote

import os
import six

from . import URIError
from . import urlparse
from . import _

import logging
log = logging.getLogger(__name__)


def _EnsureUnicode(data):
    assert(isinstance(data, (six.text_type, six.binary_type)))
    if not isinstance(data, six.text_type):
        return data.decode('utf-8')
    return data


def _EnsureUTF8(data):
    assert(isinstance(data, (six.text_type, six.binary_type)))
    if isinstance(data, six.text_type):
        return data.encode('utf-8')
    return data


EMPTY_STRING_UNICODE = u''


EMPTY_STRING_UTF8 = b''


FRAGMENT_SEPARATOR_AT = u'@'


FRAGMENT_SEPARATOR_SHARP = u'#'


FRAGMENT_SEPARATOR_EMPTY = u''


PRIMARY_KEY_SEPARATOR_AT = b'@'


PRIMARY_KEY_SEPARATOR_SHARP = b'#'


PRIMARY_KEY_SEPARATOR_EMPTY = b''


SCHEME_MUJIN = u'mujin'


SCHEME_FILE = u'file'


def _Unquote(primarykey):
    assert(isinstance(primarykey, six.binary_type))
    if six.PY3:
        # python3 unquote seems to be expecting unicode input
        return _EnsureUnicode(unquote(primarykey.decode('ascii')))
    else:
        return _EnsureUnicode(unquote(primarykey))


def _Quote(primarykey):
    assert(isinstance(primarykey, six.text_type))
    if six.PY3:
        # python3 quote seems to deal with unicode input
        return _EnsureUTF8(quote(primarykey))
    else:
        return _EnsureUTF8(quote(_EnsureUTF8(primarykey)))


def _ParseURI(uri, fragmentseparator):
    u""" Mujin uri is unicode and special characters like  #, ? and @ will be part of the path

    input:
        uri: a unicode str
        fragmentseparator: the separator to find the framgent
    output:
        ParseResult object which has the utf-8 decoded path part.

    uri will include 5 parts <scheme>://<netloc>/<path>?<query>#<fragment>
    mujinuri only have scheme which is mujin:/ , other scheme will use standard python library to parse.
    mujinuri will not have  # as fragment part because we use @ as separator to separate lie abc.mujin.dae@body0_motion

    >>> print(_ParseURI(u'mujin:/测试_test.mujin.dae', fragmentseparator=FRAGMENT_SEPARATOR_AT).path)
    /测试_test.mujin.dae
    >>> _ParseURI(u'mujin:/测试_test.mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_EMPTy).fragment
    ''
    >>> print(_ParseURI(u'mujin:/测试_test.mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_SHARP).path)
    /测试_test.mujin.dae@body0_motion
    """
    uri = _EnsureUnicode(uri)
    scheme, rest = uri.split(u':', 1)
    if scheme != SCHEME_MUJIN:
        # if scheme is not mujin specified, use the standard uri parse
        # TODO: figure out who calls this with non-mujin scheme
        # TODO: simon claim that there is conversion between mujin scheme and file scheme, all of them are done inside openrave, please     verify, maybe remove this case
        if scheme != SCHEME_FILE:
            raise URIError(_('scheme not supported %r: %s') % (scheme, uri))
        # for rfc urlparse, make sure fragment_separator is #
        # if fragmentseparator != FRAGMENT_SEPARATOR_SHARP:
        #     raise URIError(_('fragment separator %r not supported for current scheme: %s') % (fragmentseparator, uri))
        r = urlparse.urlparse(uri, allow_fragments=bool(fragmentseparator))
        return urlparse.ParseResult(
            scheme=_EnsureUnicode(r.scheme),
            netloc=_EnsureUnicode(r.netloc),
            path=_EnsureUnicode(r.path),
            params=_EnsureUnicode(r.params),
            query=_EnsureUnicode(r.query),
            fragment=_EnsureUnicode(r.fragment),
        )  # make all uri path, no matter what scheme it is, to be unicode.

    # it's a mujinuri
    if rest.startswith(u'//'):
        # usually we need to split hostname from url
        # for now mujin uri doesn't have definition of hostname in uri
        raise URIError(_('mujin scheme has no hostname defined %s') % uri)

    if fragmentseparator:
        # split by the last appeared fragmentseparator
        separatorindex = rest.rfind(fragmentseparator)
        if separatorindex >= 0:
            path = rest[:separatorindex]
            fragment = rest[separatorindex + 1:]
        else:
            path = rest
            fragment = EMPTY_STRING_UNICODE
    else:
        path = rest
        fragment = EMPTY_STRING_UNICODE

    return urlparse.ParseResult(
        scheme=scheme,
        netloc=EMPTY_STRING_UNICODE,
        path=path,
        params=EMPTY_STRING_UNICODE,
        query=EMPTY_STRING_UNICODE,
        fragment=fragment,
    )


def _UnparseURI(uriparts, fragmentseparator):
    u""" compose a uri. This function will call urlunparse if scheme is not mujin.

    uriparts is a ParseResult or a tuple which has six parts (scheme, netloc, path, params, query, fragment)

    input:
        uriparts: a six parts tuple include scheme, netloc, url/path, params, query and fragment
    output:
        a utf-8 decode uri string

    >>> print(_UnparseURI(('mujin', '', u'测试_test.mujin.dae', '', '', 'body0_motion'), fragmentseparator=FRAGMENT_SEPARATOR_AT))
    mujin:/\u6d4b\u8bd5_test.mujin.dae@body0_motion
    """
    scheme, netloc, path, params, query, fragment = uriparts  # change every parts into unicode.
    if scheme != SCHEME_MUJIN:
        # TODO: also verify who calls this with non-mujin scheme
        if scheme != SCHEME_FILE:
            raise URIError(_('scheme not supported %r: %r') % (scheme, uriparts))
        # for rfc urlparse, make sure fragment_separator is  #
        if fragmentseparator != FRAGMENT_SEPARATOR_SHARP:
            raise URIError(_('fragment separator %r not supported for current scheme: %r') % (fragmentseparator, uriparts))
        return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))  # urlunparse will return unicode if any of the parts is unicode

    assert(len(netloc) == 0)
    assert(len(params) == 0)
    assert(len(query) == 0)
    if path and not path.startswith(u'/'):
        path = '/' + path
    if fragment:
        assert(fragmentseparator in (FRAGMENT_SEPARATOR_AT, FRAGMENT_SEPARATOR_SHARP))
        path = path + fragmentseparator + fragment
    return scheme + u':' + path


def GetSchemeFromURI(uri, **kwargs):
    u""" Return the scheme of URI

    >>> GetSchemeFromURI('mujin:/test.mujin.dae')
    u'mujin'
    >>> GetSchemeFromURI('file:/test.mujin.dae')
    u'file'
    """
    return MujinResourceIdentifier(uri=uri, **kwargs).scheme


def GetFragmentFromURI(uri, **kwargs):
    u""" Return the fragment of URI
    >>> GetFragmentFromURI(u'mujin:/测试_test.mujin.dae', fragmentseparator=FRAGMENT_SEPARATOR_AT)
    ''
    >>> GetFragmentFromURI(u'mujin:/测试_test.mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_AT)
    u'body0_motion'
    >>> GetFragmentFromURI(u'mujin:/测试_test.mujin.dae#body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_AT)
    ''
    >>> GetFragmentFromURI(u'mujin:/测试_test.mujin.dae#body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_SHARP)
    u'body0_motion'
    """
    return MujinResourceIdentifier(uri=uri, **kwargs).fragment


def GetPrimaryKeyFromURI(uri, **kwargs):
    u"""
    input:
        uri: a mujin scheme uri which is utf-8 decoded unicode.
    output:
        primarykey is utf-8 encoded and quoted.

    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_AT, primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT)
    '%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion'
    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_AT, primarykeyseparator=PRIMARY_KEY_SEPARATOR_SHARP)
    '%E6%B5%8B%E8%AF%95_test..mujin.dae#body0_motion'
    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_SHARP, primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT)
    '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'
    >>> GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_SHARP, primarykeyseparator=PRIMARY_KEY_SEPARATOR_SHARP)
    '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'
    """
    if uri is None or len(uri) == 0:
        return EMPTY_STRING_UTF8

    return MujinResourceIdentifier(uri=uri, **kwargs).primarykey


def GetPrimaryKeyFromFilename(filename, **kwargs):
    """  extract primarykey from filename .
    input:
        filename: a utf-8 decoded unicode without quote. need to remove mujinpath if it's given.

    >>> GetPrimaryKeyFromFilename('/data/detection/测试_test.mujin.dae', '/data/detection')
    '%E6%B5%8B%E8%AF%95_test.mujin.dae'
    >>> GetPrimaryKeyFromFilename('/data/u/mujin/测试_test.mujin.dae', '/data/detection')
    '/data/u/mujin/%E6%B5%8B%E8%AF%95_test.mujin.dae'
    >>> GetPrimaryKeyFromFilename('/abcdefg/test.mujin.dae', '/abc')
    '/abcdefg/test.mujin.dae'
    """
    return MujinResourceIdentifier(filename=filename, **kwargs).primarykey


def GetURIFromURI(uri, newfragmentseparator, **kwargs):
    """ Compose a new uri from old one
    input:
        uri: a utf-8 decoded unicode uri string.
        fragmentseparator: the separator used in old uri
        newfragmentseparator:  the new fragment separator used in new uri.
    output:
        uri: a utf-8 decoded unicode uri string.

    >>> GetURIFromURI(u'mujin:/test.mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_AT, newfragmentseparator=FRAGMENT_SEPARATOR_SHARP)
    u'mujin:/test.mujin.dae#body0_motion'
    >>> GetURIFromURI(u'mujin:/test.mujin.dae@body0_motion', fragmentseparator=FRAGMENT_SEPARATOR_AT, newfragmentseparator=FRAGMENT_SEPARATOR_EMPTY)
    u'mujin:/test.mujin.dae'
    """
    mri = MujinResourceIdentifier(uri=uri, **kwargs)
    if newfragmentseparator:
        mri = mri.WithFragmentSeparator(newfragmentseparator)
    else:
        mri = mri.WithoutFragment()
    return mri.uri


def GetURIFromPrimaryKey(pk, **kwargs):
    """Given the encoded primary key (utf-8 encoded and quoted), returns the unicode URL.
    input:

    >>> print(GetURIFromPrimaryKey('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT, fragmentseparator=FRAGMENT_SEPARATOR_SHARP))
    mujin:/测试_test..mujin.dae#body0_motion
    >>> print(GetURIFromPrimaryKey('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT, fragmentseparator=FRAGMENT_SEPARATOR_AT))
    mujin:/测试_test..mujin.dae@body0_motion
    """
    return MujinResourceIdentifier(primarykey=pk, **kwargs).uri


def GetURIFromFilename(filename, **kwargs):
    """ Compose a mujin uri from filename.

    >>> GetURIFromFilename(u'/data/detection/test.mujin.dae', u'/data/detection')
    u'mujin:/test.mujin.dae'
    >>> GetURIFromFilename(u'/data/detection/test.mujin.dae', u'/dat')
    u'mujin:/data/detection/test.mujin.dae'
    """
    return MujinResourceIdentifier(filename=filename, **kwargs).uri


def GetFilenameFromPrimaryKey(pk, **kwargs):
    u""" return filename from primary key
    input:
        pk: utf-8 encoded str.

    output:
        filename: utf-8 decoded unicode

    >>> print(GetFilenameFromPrimaryKey('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', FRAGMENT_SEPARATOR_AT))
    测试_test..mujin.dae
    """
    return MujinResourceIdentifier(primarykey=pk, **kwargs).filename


def GetFilenameFromURI(uri, **kwargs):
    u"""returns the filesystem path that the URI points to.

    input:
        uri: a utf-8 decoded unicode. if uri is mujin scheme, will join mujin path. otherwise it will directly use parsed path result.

    output:
        filename: a utf-8 decode unicode

    >>> print(GetFilenameFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae',u'/var/www/media/u/testuser')[1])
    /var/www/media/u/testuser/検証動作1_121122.mujin.dae
    """
    return MujinResourceIdentifier(uri=uri, **kwargs).filename


def GetFilenameFromPartType(parttype, **kwargs):
    u""" Unquote parttype to get filename, if withsuffix is True, add the .mujin.dae suffix

    input:
        parttype: a utf-8 decoded unicode
    output:
        filename: a utf-8 decoded unicode

    >>> print(GetFilenameFromPartType(u'测试_test', suffix='.tar.gz'))
    测试_test.tar.gz
    >>> print(GetFilenameFromPartType(u'测试_test', suffix=''))
    测试_test
    """
    return MujinResourceIdentifier(parttype=parttype, **kwargs).filename


def GetPartTypeFromPrimaryKey(pk, **kwargs):
    u""" return a unicode partype
    input:
        pk: a utf-8 encoded str(quoted).
    output:
        parttype: a utf-8 decoded unicode

    >>> print(GetPartTypeFromPrimaryKey('%E6%B5%8B%E8%AF%95_test.mujin.dae'))
    测试_test
    """
    return MujinResourceIdentifier(primarykey=pk, **kwargs).parttype


def GetPrimaryKeyFromPartType(parttype, **kwargs):
    u"""

    input:
        parttype: a utf-8 decoded unicode

    output:
        pk: a utf-8 encoded str (quoted).

    >>> GetPrimaryKeyFromPartType(u'测试_test')
    '%E6%B5%8B%E8%AF%95_test.mujin.dae'
    """
    return MujinResourceIdentifier(parttype=parttype, **kwargs).primarykey


def GetPartTypeFromFilename(filename, **kwargs):
    u"""
    input:
        filename: a utf-8 decoded unicode
    output:
        pk: a utf-8 encoded str (quoted)

    >>> print(GetPartTypeFromFilename(u'/data/detection/测试_test.mujin.dae', mujinpath=u'/data/detection', suffix=u'.mujin.dae'))
    测试_test
    >>> print(GetPartTypeFromFilename(u'/data/detection/测试_test.mujin.dae', mujinpath=u'/data/dete', suffix=u'.mujin.dae'))
    /data/detection/测试_test
    """
    return MujinResourceIdentifier(filename=filename, **kwargs).parttype


class MujinResourceIdentifier(object):
    _fragmentseparator = FRAGMENT_SEPARATOR_EMPTY
    _primarykeyseparator = PRIMARY_KEY_SEPARATOR_EMPTY
    _suffix = EMPTY_STRING_UNICODE
    _scheme = SCHEME_MUJIN
    _mujinpath = EMPTY_STRING_UNICODE
    _primarykey = EMPTY_STRING_UTF8
    _fragment = EMPTY_STRING_UNICODE

    def __init__(self, scheme=SCHEME_MUJIN, fragment=EMPTY_STRING_UNICODE, uri=EMPTY_STRING_UNICODE, primarykey=EMPTY_STRING_UTF8, parttype=EMPTY_STRING_UNICODE, filename=EMPTY_STRING_UNICODE, suffix=EMPTY_STRING_UNICODE, mujinpath=EMPTY_STRING_UNICODE, fragmentseparator=FRAGMENT_SEPARATOR_EMPTY, primarykeyseparator=PRIMARY_KEY_SEPARATOR_EMPTY):

        self.mujinpath = mujinpath
        self.scheme = scheme
        self.fragment = fragment
        self.suffix = suffix
        self.fragmentseparator = fragmentseparator
        self.primarykeyseparator = primarykeyseparator

        if primarykey:
            self._InitFromPrimaryKey(_EnsureUTF8(primarykey))
        elif uri:
            self._InitFromURI(_EnsureUnicode(uri))
        elif parttype:
            self._InitFromPartType(_EnsureUnicode(parttype))
        elif filename:
            self._InitFromFilename(_EnsureUnicode(filename))
        else:
            raise URIError(_('Lack of parameters. initialization must include one of uri, primarykey, parttype or filename'))

    def _InitFromURI(self, uri):
        parsedUri = _ParseURI(uri, fragmentseparator=self._fragmentseparator)

        self._scheme = parsedUri.scheme
        self._fragment = parsedUri.fragment
        filename = ''
        if self._scheme == 'file':
            commonPrefix = os.path.commonprefix([self._mujinpath, parsedUri.path])
            if commonPrefix != self._mujinpath:
                raise URIError(_('scheme is file, but file absolute path is different from given mujinpath'))
            filename = parsedUri.path[len(self._mujinpath):]
        elif self._scheme == 'mujin':
            filename = parsedUri.path[1:]
        else:
            raise URIError(_('scheme %s isn\'t supported from uri %r') % (parsedUri.scheme, uri))
        self._InitFromFilename(filename)

    def _InitFromPrimaryKey(self, primarykey):
        if self._primarykeyseparator:
            # try to de-frag
            index = primarykey.rfind(self._primarykeyseparator)
            if index >= 0:
                self._primarykey = primarykey[:index]
                self._fragment = _EnsureUnicode(primarykey[index + 1:])
            else:
                self._primarykey = primarykey
        else:
            self._primarykey = primarykey

        if self._primarykey.endswith(b'.mujin.dae'):
            self._suffix = u'.mujin.dae'

    def _InitFromPartType(self, parttype):
        self._primarykey = _Quote(parttype + self._suffix)

    def _InitFromFilename(self, filename):
        if self._mujinpath and filename.startswith(self._mujinpath):
            filename = filename[len(self._mujinpath):]
        self._primarykey = _Quote(filename)

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, value):
        self._scheme = _EnsureUnicode(value)

    @property
    def fragment(self):
        return self._fragment

    @fragment.setter
    def fragment(self, value):
        self._fragment = _EnsureUnicode(value)

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self._suffix = _EnsureUnicode(value)

    @property
    def mujinpath(self):
        return self._mujinpath

    @mujinpath.setter
    def mujinpath(self, value):
        value = _EnsureUnicode(value)
        if value and not value.endswith(u'/'):
            value += u'/'
        self._mujinpath = value

    @property
    def primarykeyseparator(self):
        return self._primarykeyseparator

    @primarykeyseparator.setter
    def primarykeyseparator(self, value):
        self._primarykeyseparator = _EnsureUTF8(value)

    @property
    def fragmentseparator(self):
        return self._fragmentseparator

    @fragmentseparator.setter
    def fragmentseparator(self, value):
        self._fragmentseparator = _EnsureUnicode(value)

    @property
    def primarykey(self):
        if self._fragment and self._primarykeyseparator:
            return self._primarykey + self._primarykeyseparator + _EnsureUTF8(self._fragment)
        else:
            return self._primarykey

    @property
    def uri(self):
        """ Same as GetURIFromPrimaryKey
        """
        assert(isinstance(self._primarykey, six.binary_type))
        path = _Unquote(self._primarykey)
        return _UnparseURI((self._scheme, '', path, '', '', self._fragment), fragmentseparator=self._fragmentseparator)

    @property
    def filename(self):
        if not self._mujinpath:
            return self.parttype + self._suffix
        return os.path.join(self._mujinpath, self.parttype + self._suffix)

    @property
    def parttype(self):
        if self._suffix and self._primarykey.endswith(_EnsureUTF8(self._suffix)):
            return _Unquote(self._primarykey[:-len(_EnsureUTF8(self._suffix))])
        elif self._primarykey.endswith(b'.mujin.dae'):
            self._suffix = u'.mujin.dae'
            return _Unquote(self._primarykey[:-len(b'.mujin.dae')])
        else:
            return _Unquote(self._primarykey)

    @property
    def kwargs(self):
        return {
            'fragmentseparator': self._fragmentseparator,
            'primarykeyseparator': self._primarykeyseparator,
            'suffix': self._suffix,
            'scheme': self._scheme,
            'mujinpath': self._mujinpath,
            'primarykey': self._primarykey,
            'fragment': self._fragment,
        }

    def Clone(self, **kwargs):
        mri = MujinResourceIdentifier(**self.kwargs)
        for key, value in kwargs.items():
            setattr(mri, key, value)
        return mri

    def WithFragmentSeparator(self, fragmentseparator):
        return self.Clone(fragmentseparator=fragmentseparator)

    def WithPrimaryKeySeparator(self, primarykeyseparator):
        return self.Clone(primarykeyseparator=primarykeyseparator)

    def WithMujinPath(self, mujinpath):
        """
        >>> MujinResourceIdentifier(uri=u'file:/var/www/test.mujin.dae').filename
        u'/var/www/test.mujin.dae'
        >>> MujinResourceIdentifier(uri=u'file:/var/www/test.mujin.dae').filename
        u'/var/www/test.mujin.dae'
        >>> MujinResourceIdentifier(uri=u'file:/var/www/test.mujin.dae', mujinpath='/var/www').filename
        u'test.mujin.dae'
        >>> MujinResourceIdentifier(uri=u'file:/var/www/test.mujin.dae', mujinpath='/var/www').filename
        u'/var/www/test.mujin.dae'
        >>> MujinResourceIdentifier(primarykey='test.mujin.dae').WithMujinPath('/data/u').filename
        u'/data/u/test.mujin.dae'
        >>> MujinResourceIdentifier(primarykey='test.mujin.dae@body0_motion.mujin.dae').WithMujinPath('/data/u').filename
        u'/data/u/test.mujin.dae@body0_motion.mujin.dae'
        >>> MujinResourceIdentifier(primarykey='test.mujin.dae@body0_motion.mujin.dae', primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT).WithMujinPath('/data/u').filename
        u'/data/u/test.mujin.dae'
        >>> MujinResourceIdentifier(filename='object.tar.gz', suffix='.tar.gz').WithMujinPath('/data/u').filename
        u'/data/u/object.tar.gz'
        """
        return self.Clone(mujinpath=mujinpath)

    def WithSuffix(self, suffix):
        """
        >>> MujinResourceIdentifier(uri=u'file:/var/www/test.mujin.dae').GetWithSuffix('.tar.gz').filename
        u'/var/www/test.tar.gz'
        """
        return self.Clone(suffix=suffix)

    def WithFragment(self, fragment=EMPTY_STRING_UNICODE):
        return self.Clone(fragment=fragment)

    def WithoutFragment(self):
        """
        >>> MujinResourceIdentifier(primarykey='test.mujin.dae@body0_motion.mujin.dae', primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT).WithoutFragment().primarykey
        'test.mujin.dae'
        >>> MujinResourceIdentifier(primarykey='test.mujin.dae@body0_motion.mujin.dae', primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT).WithoutFragment().fragment
        ''
        >>> MujinResourceIdentifier(primarykey='test.mujin.dae@body0_motion.mujin.dae', primarykeyseparator=PRIMARY_KEY_SEPARATOR_AT).WithoutFragment().uri
        u'mujin:/test.mujin.dae'
        """
        return self.WithFragment()

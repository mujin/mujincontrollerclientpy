# -*- coding: utf-8 -*-
from mujincontrollerclient import uriutils


def test_GetSchemeFromURI():
    assert uriutils.GetSchemeFromURI('mujin:/test.mujin.dae') == u'mujin'
    assert uriutils.GetSchemeFromURI('file:/test.mujin.dae') == u'file'


def test_GetFragmentFromURI():
    assert uriutils.GetFragmentFromURI(u'mujin:/测试_test.mujin.dae', fragmentseparator='@') == ''
    assert uriutils.GetFragmentFromURI(u'mujin:/测试_test.mujin.dae@body0_motion', fragmentseparator='@') == u'body0_motion'
    assert uriutils.GetFragmentFromURI(u'mujin:/测试_test.mujin.dae#body0_motion', fragmentseparator='@') == ''


def test_GetPrimaryKeyFromURI():
    assert uriutils.GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='@', primarykeyseparator='@') == '%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion'
    assert uriutils.GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='@', primarykeyseparator='#') == '%E6%B5%8B%E8%AF%95_test..mujin.dae#body0_motion'
    assert uriutils.GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='#', primarykeyseparator='@') == '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'
    assert uriutils.GetPrimaryKeyFromURI(u'mujin:/测试_test..mujin.dae@body0_motion', allowfragments=True, fragmentseparator='#', primarykeyseparator='#') == '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'


def test_GetPrimaryKeyFromFilename():
    assert uriutils.GetPrimaryKeyFromFilename(u'/data/detection/测试_test.mujin.dae', '/data/detection') == '%E6%B5%8B%E8%AF%95_test.mujin.dae'
    assert uriutils.GetPrimaryKeyFromFilename(u'/data/u/mujin/测试_test.mujin.dae', '/data/detection') == '/data/u/mujin/%E6%B5%8B%E8%AF%95_test.mujin.dae'
    assert uriutils.GetPrimaryKeyFromFilename(u'/abcdefg/test.mujin.dae', '/abc') == '/abcdefg/test.mujin.dae'


def test_GetURIFromURI():
    assert uriutils.GetURIFromURI(u'mujin:/test.mujin.dae@body0_motion', allowfragments=True, fragmentseparator='@', keepfragment=True, newfragmentseparator='#') == u'mujin:/test.mujin.dae#body0_motion'
    assert uriutils.GetURIFromURI(u'mujin:/test.mujin.dae@body0_motion', allowfragments=True, fragmentseparator='@', keepfragment=False, newfragmentseparator='#') == u'mujin:/test.mujin.dae'


def test_GetURIFromPrimaryKey():
    assert uriutils.GetURIFromPrimaryKey('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', primarykeyseparator='@', fragmentseparator='#') == u'mujin:/测试_test..mujin.dae#body0_motion'


def test_GetURIFromFilename():
    assert uriutils.GetURIFromFilename(u'/data/detection/test.mujin.dae', u'/data/detection') == u'mujin:/test.mujin.dae'
    assert uriutils.GetURIFromFilename(u'/data/detection/test.mujin.dae', u'/dat') == u'mujin:/data/detection/test.mujin.dae'


def test_GetFilenameFromPrimaryKey():
    assert uriutils.GetFilenameFromPrimaryKey('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', '@') == u'测试_test..mujin.dae'


def test_GetFilenameFromURI():
    assert uriutils.GetFilenameFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae', u'/var/www/media/u/testuser')[1] == u'/var/www/media/u/testuser/検証動作1_121122.mujin.dae'


def test_GetFilenameFromPartType():
    assert uriutils.GetFilenameFromPartType(u'测试_test', suffix='.tar.gz') == u'测试_test.tar.gz'


def test_GetPartTypeFromPrimaryKey():
    assert uriutils.GetPartTypeFromPrimaryKey('%E6%B5%8B%E8%AF%95_test.mujin.dae') == u'测试_test'


def test_GetPrimaryKeyFromPartType():
    assert uriutils.GetPrimaryKeyFromPartType(u'测试_test') == '%E6%B5%8B%E8%AF%95_test.mujin.dae'


def test_GetPartTypeFromFilename():
    assert uriutils.GetPartTypeFromFilename(u'/data/detection/测试_test.mujin.dae', mujinpath='/data/detection', suffix='.mujin.dae') == u'测试_test'
    assert uriutils.GetPartTypeFromFilename(u'/data/detection/测试_test.mujin.dae', mujinpath='/data/dete', suffix='.mujin.dae') == u'/data/detection/测试_test'

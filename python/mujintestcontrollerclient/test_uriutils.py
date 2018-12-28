# -*- coding: utf-8 -*-

import pytest

from mujincontrollerclient import uriutils

@pytest.mark.parametrize('uri, expected', [
    ('mujin:/test.mujin.dae', u'mujin'),
    ('file:/test.mujin.dae', u'file'),
])
def test_GetSchemeFromURI(uri, expected):
    assert uriutils.GetSchemeFromURI(uri) == expected

@pytest.mark.parametrize('uri, fragmentseparator, expected', [
    (u'mujin:/测试_test.mujin.dae', '@', u''),
    (u'mujin:/测试_test.mujin.dae@body0_motion', '@', u'body0_motion'),
    (u'mujin:/测试_test.mujin.dae#body0_motion', '@', u''),
])
def test_GetFragmentFromURI(uri, fragmentseparator, expected):
    uriutils.GetFragmentFromURI(uri, fragmentseparator=fragmentseparator) == expected


@pytest.mark.parametrize('uri, allowfragments, fragmentseparator, primarykeyseparator, expected', [
    (u'mujin:/测试_test..mujin.dae@body0_motion', True, '@', '@', '%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion'),
    (u'mujin:/测试_test..mujin.dae@body0_motion', True, '@', '#', '%E6%B5%8B%E8%AF%95_test..mujin.dae#body0_motion'),
    (u'mujin:/测试_test..mujin.dae@body0_motion', True, '#', '@', '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'),
    (u'mujin:/测试_test..mujin.dae@body0_motion', True, '#', '#', '%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'),
])
def test_GetPrimaryKeyFromURI(uri, allowfragments, fragmentseparator, primarykeyseparator, expected):
    assert uriutils.GetPrimaryKeyFromURI(uri, allowfragments=allowfragments, fragmentseparator=fragmentseparator, primarykeyseparator=primarykeyseparator) == expected

@pytest.mark.parametrize('filename, mujinpath, expected', [
    (u'/data/detection/测试_test.mujin.dae', '/data/detection', '%E6%B5%8B%E8%AF%95_test.mujin.dae'),
    (u'/data/u/mujin/测试_test.mujin.dae', '/data/detection', '/data/u/mujin/%E6%B5%8B%E8%AF%95_test.mujin.dae'),
    (u'/abcdefg/test.mujin.dae', '/abc', '/abcdefg/test.mujin.dae'),
])
def test_GetPrimaryKeyFromFilename(filename, mujinpath, expected):
    assert uriutils.GetPrimaryKeyFromFilename(filename, mujinpath=mujinpath) == expected

@pytest.mark.parametrize('uri, allowfragments, fragmentseparator, keepfragment, newfragmentseparator, expected', [
    (u'mujin:/test.mujin.dae@body0_motion', True, '@', True, '#', u'mujin:/test.mujin.dae#body0_motion'),
    (u'mujin:/test.mujin.dae@body0_motion', True, '@', False, '#', u'mujin:/test.mujin.dae'),
])
def test_GetURIFromURI(uri, allowfragments, fragmentseparator, keepfragment, newfragmentseparator, expected):
    assert uriutils.GetURIFromURI(u'mujin:/test.mujin.dae@body0_motion', allowfragments=allowfragments, fragmentseparator=fragmentseparator, keepfragment=keepfragment, newfragmentseparator=newfragmentseparator) == expected

@pytest.mark.parametrize('pk, primarykeyseparator, fragmentseparator, expected', [
    ('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', '@', '#', u'mujin:/测试_test..mujin.dae#body0_motion'),
])
def test_GetURIFromPrimaryKey(pk, primarykeyseparator, fragmentseparator, expected):
    assert uriutils.GetURIFromPrimaryKey(pk, primarykeyseparator=primarykeyseparator, fragmentseparator=fragmentseparator) == expected


@pytest.mark.parametrize('filename, mujinpath, expected', [
    (u'/data/detection/test.mujin.dae', u'/data/detection', u'mujin:/test.mujin.dae'),
    (u'/data/detection/test.mujin.dae', u'/dat', u'mujin:/data/detection/test.mujin.dae'),
])
def test_GetURIFromFilename(filename, mujinpath, expected):
    assert uriutils.GetURIFromFilename(filename, mujinpath=mujinpath) == expected

@pytest.mark.parametrize('pk, primarykeyseparator, expected', [
    ('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', '@', u'测试_test..mujin.dae'),
])
def test_GetFilenameFromPrimaryKey(pk, primarykeyseparator, expected):
    assert uriutils.GetFilenameFromPrimaryKey(pk, primarykeyseparator=primarykeyseparator) == expected


@pytest.mark.parametrize('uri, mujinpath, expected', [
    (u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae', u'/var/www/media/u/testuser', u'/var/www/media/u/testuser/検証動作1_121122.mujin.dae'),
])
def test_GetFilenameFromURI(uri, mujinpath, expected):
    assert uriutils.GetFilenameFromURI(uri, mujinpath=mujinpath)[1] == expected

@pytest.mark.parametrize('partType, suffix, expected', [
    (u'测试_test', '.tar.gz', u'测试_test.tar.gz'),
])
def test_GetFilenameFromPartType(partType, suffix, expected):
    assert uriutils.GetFilenameFromPartType(partType, suffix=suffix) == expected


@pytest.mark.parametrize('pk, expected', [
    ('%E6%B5%8B%E8%AF%95_test.mujin.dae', u'测试_test'),
])
def test_GetPartTypeFromPrimaryKey(pk, expected):
    assert uriutils.GetPartTypeFromPrimaryKey(pk) == expected

@pytest.mark.parametrize('partType, expected', [
    (u'测试_test', '%E6%B5%8B%E8%AF%95_test.mujin.dae'),
])
def test_GetPrimaryKeyFromPartType(partType, expected):
    assert uriutils.GetPrimaryKeyFromPartType(partType) == expected


@pytest.mark.parametrize('filename, mujinpath, suffix, expected', [
    (u'/data/detection/测试_test.mujin.dae', '/data/detection', '.mujin.dae', u'测试_test'),
    (u'/data/detection/测试_test.mujin.dae', '/data/dete', '.mujin.dae',u'/data/detection/测试_test'),
])
def test_GetPartTypeFromFilename(filename, mujinpath, suffix, expected):
    assert uriutils.GetPartTypeFromFilename(filename, mujinpath=mujinpath, suffix=suffix) == expected

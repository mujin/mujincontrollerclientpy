# -*- coding: utf-8 -*-

import pytest

from mujincontrollerclient import uriutils


@pytest.mark.parametrize('uri, expected', [
    (u'mujin:/test.mujin.dae', u'mujin'),
    (u'file:/test.mujin.dae', u'file'),
])
def test_GetSchemeFromURI(uri, expected):
    assert uriutils.GetSchemeFromURI(uri) == expected


@pytest.mark.parametrize('uri, fragmentSeparator, expected', [
    (u'mujin:/测试_test.mujin.dae', uriutils.FRAGMENT_SEPARATOR_AT, u''),
    (u'mujin:/测试_test.mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_AT, u'body0_motion'),
    (u'mujin:/测试_test.mujin.dae#body0_motion', uriutils.FRAGMENT_SEPARATOR_AT, u''),
])
def test_GetFragmentFromURI(uri, fragmentSeparator, expected):
    assert uriutils.GetFragmentFromURI(uri, fragmentSeparator=fragmentSeparator) == expected


@pytest.mark.parametrize('uri, fragmentSeparator, primaryKeySeparator, expected', [
    (u'mujin:/测试_test..mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_AT, uriutils.PRIMARY_KEY_SEPARATOR_AT, b'%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion'),
    (u'mujin:/测试_test..mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_AT, uriutils.PRIMARY_KEY_SEPARATOR_SHARP, b'%E6%B5%8B%E8%AF%95_test..mujin.dae#body0_motion'),
    (u'mujin:/测试_test..mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_SHARP, uriutils.PRIMARY_KEY_SEPARATOR_AT, b'%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'),
    (u'mujin:/测试_test..mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_SHARP, uriutils.PRIMARY_KEY_SEPARATOR_SHARP, b'%E6%B5%8B%E8%AF%95_test..mujin.dae%40body0_motion'),
    (u'mujin:/private/s/gittest.mujin.dae', uriutils.FRAGMENT_SEPARATOR_SHARP, uriutils.PRIMARY_KEY_SEPARATOR_SHARP, b'private%2Fs%2Fgittest.mujin.dae'),
])
def test_GetPrimaryKeyFromURI(uri, fragmentSeparator, primaryKeySeparator, expected):
    assert uriutils.GetPrimaryKeyFromURI(uri, fragmentSeparator=fragmentSeparator, primaryKeySeparator=primaryKeySeparator) == expected


@pytest.mark.parametrize('filename, mujinPath, expected', [
    (u'/data/detection/测试_test.mujin.dae', u'/data/detection', b'%E6%B5%8B%E8%AF%95_test.mujin.dae'),
    (u'/data/u/mujin/测试_test.mujin.dae', u'/data/detection', b'%2Fdata%2Fu%2Fmujin%2F%E6%B5%8B%E8%AF%95_test.mujin.dae'),
    (u'/abcdefg/test.mujin.dae', u'/abc', b'%2Fabcdefg%2Ftest.mujin.dae'),
    (u'/data/media/mujin/private/s/gittest.mujin.dae', u'/data/media/mujin', b'private%2Fs%2Fgittest.mujin.dae'),
])
def test_GetPrimaryKeyFromFilename(filename, mujinPath, expected):
    assert uriutils.GetPrimaryKeyFromFilename(filename, mujinPath=mujinPath) == expected


@pytest.mark.parametrize('uri, fragmentSeparator, newFragmentSeparator, expected', [
    (u'mujin:/test.mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_AT, uriutils.FRAGMENT_SEPARATOR_SHARP, u'mujin:/test.mujin.dae#body0_motion'),
    (u'mujin:/test.mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_AT, uriutils.FRAGMENT_SEPARATOR_EMPTY, u'mujin:/test.mujin.dae'),
])
def test_GetURIFromURI(uri, fragmentSeparator, newFragmentSeparator, expected):
    assert uriutils.GetURIFromURI(u'mujin:/test.mujin.dae@body0_motion', fragmentSeparator=fragmentSeparator, newFragmentSeparator=newFragmentSeparator) == expected


@pytest.mark.parametrize('primaryKey, primaryKeySeparator, fragmentSeparator, expected', [
    (b'%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', uriutils.PRIMARY_KEY_SEPARATOR_AT, uriutils.FRAGMENT_SEPARATOR_SHARP, u'mujin:/测试_test..mujin.dae#body0_motion'),
])
def test_GetURIFromPrimaryKey(primaryKey, primaryKeySeparator, fragmentSeparator, expected):
    assert uriutils.GetURIFromPrimaryKey(primaryKey, primaryKeySeparator=primaryKeySeparator, fragmentSeparator=fragmentSeparator) == expected


@pytest.mark.parametrize('filename, mujinPath, expected', [
    (u'/data/detection/test.mujin.dae', u'/data/detection', u'mujin:/test.mujin.dae'),
    (u'/data/detection/test.mujin.dae', u'/dat', u'mujin:/data/detection/test.mujin.dae'),
])
def test_GetURIFromFilename(filename, mujinPath, expected):
    assert uriutils.GetURIFromFilename(filename, mujinPath=mujinPath) == expected


@pytest.mark.parametrize('primaryKey, primaryKeySeparator, expected', [
    ('%E6%B5%8B%E8%AF%95_test..mujin.dae@body0_motion', uriutils.PRIMARY_KEY_SEPARATOR_AT, u'测试_test..mujin.dae'),
])
def test_GetFilenameFromPrimaryKey(primaryKey, primaryKeySeparator, expected):
    assert uriutils.GetFilenameFromPrimaryKey(primaryKey, primaryKeySeparator=primaryKeySeparator) == expected


@pytest.mark.parametrize('uri, mujinPath, fragmentSeparator, expected', [
    (u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae', u'/var/www/media/u/testuser', uriutils.FRAGMENT_SEPARATOR_EMPTY, u'/var/www/media/u/testuser/検証動作1_121122.mujin.dae'),
])
def test_GetFilenameFromURI(uri, mujinPath, fragmentSeparator, expected):
    assert uriutils.GetFilenameFromURI(uri, mujinPath=mujinPath, fragmentSeparator=fragmentSeparator) == expected


@pytest.mark.parametrize('partType, suffix, expected', [
    (u'测试_test', u'.tar.gz', u'测试_test.tar.gz'),
])
def test_GetFilenameFromPartType(partType, suffix, expected):
    assert uriutils.GetFilenameFromPartType(partType, suffix=suffix) == expected


@pytest.mark.parametrize('primaryKey, expected', [
    (b'%E6%B5%8B%E8%AF%95_test.mujin.dae', u'测试_test'),
])
def test_GetPartTypeFromPrimaryKey(primaryKey, expected):
    assert uriutils.GetPartTypeFromPrimaryKey(primaryKey) == expected


@pytest.mark.parametrize('partType, suffix, expected', [
    (u'测试_test', u'.mujin.dae', b'%E6%B5%8B%E8%AF%95_test.mujin.dae'),
])
def test_GetPrimaryKeyFromPartType(partType, suffix, expected):
    assert uriutils.GetPrimaryKeyFromPartType(partType, suffix=suffix) == expected


@pytest.mark.parametrize('partType, suffix, expected', [
    (u'测试_test', u'.mujin.dae', u'mujin:/测试_test.mujin.dae'),
])
def test_GetURIFromPartType(partType, suffix, expected):
    assert uriutils.GetURIFromPartType(partType, suffix=suffix) == expected


@pytest.mark.parametrize('filename, mujinPath, suffix, expected', [
    (u'/data/detection/测试_test.mujin.dae', u'/data/detection', u'.mujin.dae', u'测试_test'),
    (u'/data/detection/测试_test.mujin.dae', u'/data/dete', u'.mujin.dae', u'/data/detection/测试_test'),
])
def test_GetPartTypeFromFilename(filename, mujinPath, suffix, expected):
    assert uriutils.GetPartTypeFromFilename(filename, mujinPath=mujinPath, suffix=suffix) == expected

@pytest.mark.parametrize('uri, fragmentSeparator,  expected', [
    (u'mujin:/测试_test.mujin.dae@body0_motion', uriutils.FRAGMENT_SEPARATOR_AT, u'测试_test'),
    (u'mujin:/测试_test.mujin.dae', uriutils.FRAGMENT_SEPARATOR_AT, u'测试_test'),
    (u'mujin:/test.mujin.dae', uriutils.FRAGMENT_SEPARATOR_AT, u'test'),
])
def test_GetPartTypeFromURI(uri, fragmentSeparator, expected):
    assert uriutils.GetPartTypeFromURI(uri, fragmentSeparator=fragmentSeparator) == expected

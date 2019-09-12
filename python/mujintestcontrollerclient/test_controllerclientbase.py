# -*- coding: utf-8 -*-

import pytest
import requests_mock

from mujincontrollerclient.controllerclientbase import ControllerClient


@pytest.mark.parametrize('url, username, password', [
    ('http://controller', 'mujin', 'mujin'),
    ('http://controller:8080', 'mujin', 'mujin'),
    ('http://127.0.0.1', 'testuser', 'pass'),
    ('http://127.0.0.1:8080', 'testuser', 'pass'),
])
def test_PingAndLogin(url, username, password):
    with requests_mock.Mocker() as mock:
        mock.head('%s/u/%s/' % (url, username))
        controllerclient = ControllerClient(url, username, password)
        controllerclient.Ping()
        controllerclient.Login()
        assert controllerclient.IsLoggedIn()


def test_RestartController():
    with requests_mock.Mocker() as mock:
        mock.post('http://controller/restartserver/')
        ControllerClient('http://controller', 'mujin', 'mujin').RestartController()


def test_GetScenes():
    with requests_mock.Mocker() as mock:
        mock.get('http://controller/api/v1/scene/?format=json&limit=0&offset=0', json={
            'objects': [],
            'meta': {
                'total_count': 101,
                'limit': 20,
                'offset': 0,
            },
        })
        scenes = ControllerClient('http://controller', 'mujin', 'mujin').GetScenes()
        assert len(scenes) == 0
        assert scenes.offset == 0
        assert scenes.limit == 20
        assert scenes.totalCount == 101

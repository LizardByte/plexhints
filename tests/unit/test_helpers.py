# -*- coding: utf-8 -*-

# lib imports
import pytest

# local imports
from plexhints import _helpers


def test_check_port_elevated(elevated_policy):
    # ensure no exception is raised
    _helpers.check_port(url='http://localhost:32400/')


def test_check_port_not_elevated(non_elevated_policy):
    with pytest.raises(Exception):
        _helpers.check_port(url='http://localhost:32400/')


def test_http_request():
    # test with method = None
    test_response = _helpers.http_request(
        url='https://github.com/LizardByte/plexhints',
        cache_time=None,
        method=None,
    )
    assert test_response.status_code == 200

    # test with method = 'GET'
    test_response = _helpers.http_request(
        url='https://github.com/LizardByte/plexhints',
        cache_time=None,
        method='GET',
    )
    assert test_response.status_code == 200

    # test with cache_time = 10
    test_response = _helpers.http_request(
        url='https://github.com/LizardByte/plexhints',
        cache_time=10,
        method='GET',
    )

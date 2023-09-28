# -*- coding: utf-8 -*-

# standard imports
from typing import Callable

# lib imports
import pytest

# local imports
from plexhints import proxy_kit


def test_proxy_object_generator():
    generator = proxy_kit.proxy_object_generator(proxy_name='Pytest')
    assert isinstance(generator, Callable)


@pytest.fixture(scope='function')
def proxy_kit_fixture():
    return proxy_kit._ProxyKit()


@pytest.mark.parametrize('proxy_name', ['Preview', 'Media', 'LocalFile', 'Remote'])
def test_proxy_kit(proxy_kit_fixture, proxy_name):
    assert hasattr(proxy_kit_fixture, proxy_name)
    assert isinstance(getattr(proxy_kit_fixture, proxy_name), Callable)

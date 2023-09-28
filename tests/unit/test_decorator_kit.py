# -*- coding: utf-8 -*-

# local imports
from plexhints import decorator_kit


def test_handler():
    handler = decorator_kit.handler(prefix='/video/example', name='Example')
    assert handler


def test_indirect():
    indirect = decorator_kit.indirect(func=None)
    assert indirect


def test_route(caplog):
    assert decorator_kit.route(path='/video/example/myRoute/play')
    assert decorator_kit.route(path='/video/example/myRoute/play', method='GET')
    assert decorator_kit.route(path='/video/example/myRoute/play', method='PUT')
    captured = caplog
    assert not captured.text

    # this should write an error message to stdout
    assert decorator_kit.route(path='/video/example/myRoute/play', method='POST')
    captured = caplog
    assert captured.text

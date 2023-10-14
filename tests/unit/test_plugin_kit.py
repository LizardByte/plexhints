# -*- coding: utf-8 -*-

# local imports
from plexhints import plugin_kit


def test_prefixes():
    assert isinstance(plugin_kit.Prefixes(), list)

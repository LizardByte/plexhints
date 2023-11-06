# -*- coding: utf-8 -*-
"""Constants used by plexhints."""

# Library version
MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = 2
__short_version__ = '{}.{}'.format(MAJOR_VERSION, MINOR_VERSION)
__version__ = '{}.{}'.format(__short_version__, PATCH_VERSION)

__name__ = 'plexhints'
__description__ = 'Type hinting library for Plex plugin development.'

# plex will likely never update this number... this could be used for depreciation warnings
PLEX_FRAMEWORK_VERSION = '2.6.3'

# -*- coding: utf-8 -*-
"""Constants used by plexhints."""

# Library version
MAJOR_VERSION = 0
MINOR_VERSION = 2
PATCH_VERSION = 0
__short_version__ = '%s.%s' % (MAJOR_VERSION, MINOR_VERSION)
__version__ = '%s.%s' % (__short_version__, PATCH_VERSION)

__name__ = 'plexhints'
__description__ = 'Type hinting library for Plex plugin development.'

# plex will likely never update this number... this could be used for depreciation warnings
PLEX_FRAMEWORK_VERSION = '2.6.3'

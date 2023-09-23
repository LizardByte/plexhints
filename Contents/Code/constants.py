# -*- coding: utf-8 -*-

# standard imports
import plistlib
import os

# plex debugging
try:
    import plexhints  # noqa: F401
except ImportError:
    pass
else:  # the code is running outside of Plex
    from plexhints.core_kit import Core  # core kit

# get plugin directory from core kit
plugin_directory = Core.bundle_path
if plugin_directory.endswith('test.bundle'):
    # use current directory instead, to allow for testing outside of Plex
    if os.path.basename(os.getcwd()) == 'docs':
        # use parent directory if current directory is 'docs'
        plugin_directory = os.path.dirname(os.getcwd())
    else:
        plugin_directory = os.getcwd()

# get identifier and version from Info.plist file
info_file_path = os.path.join(plugin_directory, 'Contents', 'Info.plist')
try:
    info_plist = plistlib.readPlist(pathOrFile=info_file_path)
except IOError:
    info_plist = dict(
        CFBundleIdentifier='dev.lizardbyte.plexhints',
        PlexBundleVersion='0.0.0'
    )
plugin_identifier = info_plist['CFBundleIdentifier']
version = info_plist['PlexBundleVersion']

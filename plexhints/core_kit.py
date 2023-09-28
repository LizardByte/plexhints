# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import os
import platform
import shutil
import tempfile
from typing import AnyStr

# local imports
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()

_APP_DATA_PATH = dict(
    Darwin="{}/Library/Application Support".format(os.getenv('HOME')),
    Linux="/var/lib/plexmediaserver/Library/Application Support",
    Windows="{}".format(os.getenv('LOCALAPPDATA'))
)
_PLEX_MEDIA_SERVER_PATH = dict(
    Darwin="{}/Plex Media Server".format(_APP_DATA_PATH['Darwin']),
    Linux="{}/Plex Media Server".format(_APP_DATA_PATH['Linux']),
    Windows="{}\\Plex Media Server".format(_APP_DATA_PATH['Windows']),
)
# macOS plugin log path is not based on the app data path
# https://support.plex.tv/articles/201106148-channel-log-files/
_PLUGIN_LOGS_PATH = dict(
    Darwin="{}/Library/Logs/Plex Media Server/PMS Plugin Logs".format(os.getenv('HOME')),
    Linux="{}/Logs/PMS Plugin Logs".format(_PLEX_MEDIA_SERVER_PATH['Linux']),
    Windows="{}\\Logs\\PMS Plugin Logs".format(_PLEX_MEDIA_SERVER_PATH['Windows']),
)
_PLATFORM = platform.system()
_APP_DATA_PATH = _APP_DATA_PATH[_PLATFORM]
_PLEX_MEDIA_SERVER_PATH = _PLEX_MEDIA_SERVER_PATH[_PLATFORM]
_PLUGIN_LOGS_PATH = _PLUGIN_LOGS_PATH[_PLATFORM]


class _CoreKit:
    def __init__(self):
        self.data = self.Data()
        self.storage = self.Storage()
        self.app_support_path = os.path.join(os.getenv('PLEX_APP_DATA_PATH', _PLEX_MEDIA_SERVER_PATH))
        self.bundle_path = os.path.join(self.app_support_path, 'Plug-ins', 'test.bundle')
        self.bundled_plugins_path = os.path.join(self.app_support_path, 'Plug-ins')
        self.plugin_support_path = os.path.join(self.app_support_path, 'Plug-in Support')

    class Data:
        def __init__(self):
            # todo - implement these components (see data.py)
            self.json = None
            self.xml = None
            self.pickle = None
            self.archiving = None
            self.hashing = None

    class Storage:
        def __init__(self):
            self.data_path = os.path.join('plexhints-temp', 'Data', 'test')
            self.walk = os.walk
            self.copy = shutil.copy
            self.rename = shutil.move
            self.remove = os.remove
            self.utime = os.utime
            self.dir_name = os.path.dirname
            self.last_accessed = os.path.getatime
            self.last_modified = os.path.getmtime
            self.path_sep = os.path.sep
            self.base_name = os.path.basename
            self.abs_path = os.path.abspath
            self.make_temp_dir = tempfile.mkdtemp
            self.change_dir = os.chdir
            self.current_dir = os.getcwd

            # Create a dictionary for storing file modification times.
            self._mtimes = {}

            data_items_path = os.path.join(self.data_path, 'DataItems')
            if not os.path.isdir(data_items_path):  # create directory if it doesn't exist
                os.makedirs(data_items_path)

        def load(self, filename, binary=True, mtime_key=None):
            # type: (str, bool, str) -> AnyStr
            filename = os.path.abspath(filename)

            data = None
            try:
                if binary:
                    mode = 'rb'
                else:
                    mode = 'r'
                f = open(filename, mode)
                data = f.read()
                f.close()
            except Exception:
                _Log.Exception("Exception reading file %s", filename)
                data = None
                raise
            finally:
                return data

        def save(self, filename, data, binary=True, mtime_key=None):
            # type: (str, AnyStr, bool, str) -> None
            if data is None:  # Don't attempt to save if no data was passed
                _Log.Error("Attempted to save no data to '%s' - aborting. Nothing has been saved to disk.", filename)
                return

            filename = os.path.abspath(filename)
            temp_file = '%s/._%s' % (os.path.dirname(filename), os.path.basename(filename))
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                if binary:
                    mode = 'wb'
                else:
                    mode = 'w'
                f = open(temp_file, mode)
                f.write(data if binary else str(data))
                f.close()
                if os.path.exists(filename):
                    os.remove(filename)
                shutil.move(temp_file, filename)
            except Exception:
                _Log.Exception("Exception writing to %s", filename)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                raise


Core = _CoreKit()

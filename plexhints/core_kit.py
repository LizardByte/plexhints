# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import os
import shutil
import tempfile
from typing import AnyStr

# local imports
from plexhints.log_kit import LogKit

# setup logging
Log = LogKit()


class CoreKit:
    def __init__(self):
        self.storage = self.Storage()

    class Storage:
        def __init__(self):
            self.data_path = os.path.join('plexhints', 'Data', 'test')
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

            os.makedirs(os.path.join(self.data_path, 'DataItems'))

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
                Log.Exception("Exception reading file %s", filename)
                data = None
                raise
            finally:
                return data

        def save(self, filename, data, binary=True, mtime_key=None):
            # type: (str, AnyStr, bool, str) -> None
            if data is None:  # Don't attempt to save if no data was passed
                Log.Error("Attempted to save no data to '%s' - aborting. Nothing has been saved to disk.", filename)
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
                f.write(str(data))
                f.close()
                if os.path.exists(filename):
                    os.remove(filename)
                shutil.move(temp_file, filename)
            except Exception:
                Log.Exception("Exception writing to %s", filename)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                raise

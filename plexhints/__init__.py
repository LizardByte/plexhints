# standard imports
import os
import sys

# this list is used in kits.py and prefs_kit.py
if os.path.isdir('Contents'):
    CONTENTS = ['Contents']
else:
    CONTENTS = []

# constants
ELEVATED_POLICY = False  # type: bool
GLOBAL_DEFAULT_TIMEOUT = 20.0  # type: float


# open the plugin's Plist file and see if it has an elevated policy
def plexhints_setup():
    # type: () -> bool
    """
    Read the plugin plist file and determine if plexhints should use elevated policy or not.

    Returns
    -------
    bool
        True if policy is elevated, otherwise False.

    Examples
    >>> plexhints_setup()
    ...
    """
    global ELEVATED_POLICY

    # imports prevent installation with setup.py using pip
    # local imports
    from plexhints.log_kit import _LogKit
    from plexhints.parse_kit import _PlistKit

    # setup logging
    _Log = _LogKit()

    plist_file = os.path.join(*CONTENTS + ['Info.plist'])
    if os.path.isfile(plist_file):
        with open(plist_file, mode='r') as f:
            plist_dict = _PlistKit().ObjectFromString(string=f.read())

            try:
                if plist_dict['PlexPluginCodePolicy'] == 'Elevated':
                    ELEVATED_POLICY = True
            except KeyError:
                pass

            del plist_dict
    else:
        _Log.Warn('Setting "ELEVATED_POLICY" to "False", no plist file was found at: %s' % plist_file)
        ELEVATED_POLICY = False

    return ELEVATED_POLICY


def update_sys_path():
    # type: () -> bool
    """
    This is a helper function to append the ``Libraries/Shared`` path to the system path.

    Returns
    -------
    bool
        True if path was appended, False otherwise.

    Examples
    --------
    >>> update_sys_path()
    True
    """
    contents_path = ['Contents', 'Libraries', 'Shared']
    current_directory = os.getcwd()

    directory_tests = []

    # setup directories to check... allows code to be run from subdirectories such as `docs`
    while True:
        parent_path = os.path.dirname(current_directory)
        if parent_path:
            if parent_path not in directory_tests:
                directory_tests.append(parent_path)
                current_directory = parent_path
            else:
                break
        else:
            break

    for directory in directory_tests:
        tmp_contents_path = list(contents_path)  # copy the original list
        while True:
            try:
                if os.path.isdir(os.path.join(directory, *tmp_contents_path)):
                    sys.path.append(os.path.join(directory, *tmp_contents_path))
                    return True
                else:
                    try:
                        tmp_contents_path.pop(0)
                    except IndexError:
                        return False
            except TypeError:
                continue

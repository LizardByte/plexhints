# -*- coding: utf-8 -*-

# standard imports
import os
import sys

# local imports
import plexhints


def test_plexhints_setup():
    policy = plexhints.plexhints_setup()
    assert policy, ("ELEVATED_POLICY should be True when ./Contents/Info.plist exists and has "
                    "PlexPluginCodePolicy as Elevated")


def test_update_sys_path():
    try:
        os.removedirs(os.path.join('Contents', 'Libraries', 'Shared'))
    except OSError:
        pass
    plexhints.update_sys_path()
    assert os.path.join(os.getcwd(), 'Contents', 'Libraries', 'Shared') not in sys.path, \
        "Shared path should be in sys.path"

    try:
        os.makedirs(os.path.join('Contents', 'Libraries', 'Shared'))
    except OSError:
        pass
    plexhints.update_sys_path()
    assert os.path.join(os.getcwd(), 'Contents', 'Libraries', 'Shared') in sys.path, "Shared path should be in sys.path"

    os.removedirs(os.path.join('Contents', 'Libraries', 'Shared'))

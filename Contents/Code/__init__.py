# -*- coding: utf-8 -*-

# standard imports
import os

# plex debugging
try:
    import plexhints  # noqa: F401
except ImportError:
    pass
else:  # the code is running outside of Plex
    from plexhints import plexhints_setup, update_sys_path
    plexhints_setup()  # read the plugin plist file and determine if plexhints should use elevated policy or not
    update_sys_path()  # when running outside plex, append the path

    from plexhints.decorator_kit import handler  # decorator kit
    from plexhints.log_kit import Log  # log kit

# local imports
from .constants import version


def Start():
    # type: () -> True
    """
    Start the plug-in.

    This function is called when the plug-in first starts. It can be used to perform extra initialisation tasks such as
    configuring the environment and setting default attributes. See the archived Plex documentation
    `Predefined functions
    <https://web.archive.org/web/https://dev.plexapp.com/docs/channels/basics.html#predefined-functions>`_
    for more information.

    Preferences are validated, then additional threads are started for the web server, queue, plex listener, and
    scheduled tasks.

    Returns
    -------
    True
        Always returns ``True``.

    Examples
    --------
    >>> Start()
    ...
    """
    Log.Info('plexhints, version: {}'.format(version))
    Log.Debug('plex-x-token: {}'.format(os.getenv('PLEXTOKEN', None)))
    Log.Warn(
        'This plugin should not be installed to any production Plex Media Server. It is intended for CI/CD pipelines.')
    return True


@handler(prefix='/applications/plexhints', name='plexhints ({})'.format(version))
def main():
    """
    Create the main plug-in ``handler``.

    This is responsible for displaying the plug-in in the plug-ins menu. Since we are using the ``@handler`` decorator,
    and since Plex removed menu's from plug-ins, this method does not need to perform any other function.
    """
    pass

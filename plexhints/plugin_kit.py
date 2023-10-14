# future imports
from __future__ import absolute_import  # import like python 3

# local imports
from plexhints import GLOBAL_DEFAULT_TIMEOUT

BundlePath = None  # the path to the plugin bundle
ResourcesPath = None  # the path to the Resources directory inside the plugin bundle
Identifier = None  # the reverse DNS identifier of the plugin
DataPath = None  # the path to the plugin's data directory
Debug = False  # check whether debugging is enabled

HTTP_TIMEOUT_VAR_NAME = "PLEX_MEDIA_SERVER_PLUGIN_TIMEOUT"
HTTP_DEFAULT_TIMEOUT = GLOBAL_DEFAULT_TIMEOUT

Response = {}
MimeTypes = {}
ViewGroups = {}
Dict = {}
__savedDict = {}

__pluginModule = None
__prefs = None
__prefsPath = None
__databasePath = None
__logFilePath = None
__requestHandlers = {}
__publicResources = {}


def Prefixes():
    # type: () -> list
    return list(__requestHandlers)  # use `list()` instead of `.keys()` https://stackoverflow.com/a/18552025

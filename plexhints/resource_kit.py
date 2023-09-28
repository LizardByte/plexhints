# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import os
from typing import Optional, Union

# lib imports
from deprecation import deprecated

# local imports
from plexhints import plugin_kit
from plexhints.const import PLEX_FRAMEWORK_VERSION
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()

__resourcePath = None
__sharedResourcePath = None
__publicResources = {}
__publicSharedResources = {}
__mimeTypes = None


def __load(path, binary=True):
    # type: (str, bool) -> Optional[Union[bytes, str]]
    if os.path.exists(path):
        if not binary:
            f = open(path, "r")
        else:
            f = open(path, "rb")
        resource = f.read()
        f.close()
        return resource
    return


def __expose_resource(name, contentType):
    # type: (str, str) -> bool
    if os.path.exists("%s/%s" % (__resourcePath, name)) and name not in __publicResources:
        __publicResources[name] = contentType
        _Log.Info("(Framework) Resource named '%s' of type '%s' was made public." % (name, contentType))
        return True
    else:
        return False


def __expose_shared_resource(name, contentType):
    # type: (str, str) -> bool
    if os.path.exists("%s/%s" % (__sharedResourcePath, name)) and name not in __publicSharedResources:
        __publicSharedResources[name] = contentType
        _Log.Info("(Framework) Shared resource named '%s' of type '%s' was made public." % (name, contentType))
        return True
    else:
        return False


def __real_shared_item_name(itemName):
    # type: (str) -> Optional[str]
    for ext in ["png", "jpg"]:
        item_name_with_ext = '%s.%s' % (itemName, ext)
        if os.path.exists(os.path.join(__sharedResourcePath, item_name_with_ext)):
            return item_name_with_ext
    return None


def load(itemName, binary=True):
    # type: (str, bool) -> Optional[Union[bytes, str]]
    data = __load("%s/%s" % (__resourcePath, itemName), binary)
    if data is not None:
        _Log.Info("(Framework) Loaded resource named '%s'" % itemName)
        return data


def load_shared(itemName, binary=True):
    # type: (str, bool) -> Optional[Union[bytes, str]]
    data = __load("%s/%s" % (__sharedResourcePath, itemName), binary)
    if data is not None:
        _Log.Info("(Framework) Loaded shared resource named '%s'" % itemName)
        return data


def external_path(itemName):
    # type: (str) -> Optional[str]
    if not plugin_kit.Prefixes():
        return

    if not itemName:
        return
    ext = itemName[itemName.rfind("."):]
    if ext in __mimeTypes:
        __expose_resource(itemName, __mimeTypes[ext])
    else:
        __expose_resource(itemName, "application/octet-stream")

    if itemName in __publicResources:
        return "%s/:/resources/%s" % (plugin_kit.Prefixes()[0], itemName)
    else:
        return


@deprecated(deprecated_in=None, removed_in=None, current_version=PLEX_FRAMEWORK_VERSION,
            details="Resource.SharedExternalPath() (and the 'S' alias) are deprecated. \
            All resource path generation can now be done via Resource.ExternalPath() (and the 'R' alias). \
            Please update your code.")
def shared_external_path(itemName):
    # type: (str) -> Optional[str]
    if not plugin_kit.Prefixes():
        return
    global __publicSharedResources
    global __mimeTypes
    if not itemName:
        return

    if itemName.find(".") < 0:
        itemName = __real_shared_item_name(itemName)

    if not itemName:
        return

    ext = itemName[itemName.rfind("."):]
    if ext in __mimeTypes:
        __expose_shared_resource(itemName, __mimeTypes[ext])
    else:
        __expose_shared_resource(itemName, "application/octet-stream")

    if itemName in __publicSharedResources:
        return "%s/:/sharedresources/%s" % (plugin_kit.Prefixes()[0], itemName)
    else:
        return


def mime_type_for_extension(ext):
    # type: (str) -> str
    global __mimeTypes
    try:
        return __mimeTypes[ext]
    except KeyError:
        return "application/octet-stream"


def add_mime_type(ext, mimeType):
    # type: (str, str) -> None
    global __mimeTypes
    __mimeTypes[ext] = mimeType


class _ResourceKit:
    def __init__(self):
        pass

    Load = load
    LoadShared = load_shared
    ExternalPath = external_path
    SharedExternalPath = shared_external_path
    MimeTypeForExtension = mime_type_for_extension
    AddMimeType = add_mime_type


Resource = _ResourceKit()

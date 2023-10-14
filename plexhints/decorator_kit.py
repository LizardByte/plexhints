# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
from typing import Any

# local imports
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()


def handler(prefix, name, thumb='icon-default.png', art='art-default.png'):
    # type: (str, str, str, str) -> Any
    """
    This function should always be used as a decorator. It enables the developer to register a function in their code
    as a prefix handler. Any subsequent requests with a matching prefix will be directed to that plug-in by the media
    server:

    .. code-block:: python

       @handler('/video/example', 'Example')
       def Main():
           pass

    The decorated function definition should not include any required arguments.

    Parameters
    ----------
    prefix : str
        The prefix at which to register the plug-in. All plug-ins should be registered under one of the four main
        top-level directories:

            - video
            - music
            - photos
            - applications
    name : str
        The title of the registered prefix, to be displayed in the client user interface. This can be either a string,
        or the key of a localized string.
    thumb : str
        The name of the thumbnail resource file.
    art : str
        The name of the artwork resource file.
    """
    def decorator_method(func):
        def decorator_call():
            return

    return decorator_method


def indirect(func):
    """
    This function should only be used as a decorator. It is used to specify that a function does not return data
    directly, but instead returns an ``ObjectContainer`` with a single item referring to the final location of the
    data. This is useful when the server the stream resides on requires a specific user agent string or cookies before
    it will serve the media, and these can't be computed easily or quickly.

    Using the decorator is simple:

    .. code-block:: python

       @indirect
       @route('/video/example/myRoute/play')
       def Play(x):
           ...

    The framework will automatically adjust generated callback paths and the XML returned to clients to indicate that
    the function does not return a direct response.

    Returns
    -------
    _TemplateKit.ObjectContainer
        The object container.
    """
    def decorator_call():
        return

    return indirect


def route(path, method='GET'):
    # type: (str, str) -> Any
    """
    This function should always be used as a decorator. It allows functions to be assigned routes under a registered
    prefix (e.g. ``/video/example/myRoute``). This enables the developer to give their plug-in a REST-like API with
    very little effort.

    Parameters
    ----------
    path : str
        The path for the new route.
    method
        The HTTP method the route should be assigned to, either ``GET`` or ``PUT``.

    Notes
    -----
    Route paths can include keyword arguments enclosed in braces that will be passed to the function when it is
    executed:

    .. code-block:: python

       @route('/video/example/myRoute/{x}')
       def MyFunction(x):
           print(x)
    """
    def decorator_method(func):
        def decorator_call():
            return

    allowed_methods = ['GET', 'PUT']
    if method not in allowed_methods:
        _Log.Exception('The HTTP method should be either "GET" or "PUT", not "%s"' % method)

    return decorator_method

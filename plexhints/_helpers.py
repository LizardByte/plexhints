# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import datetime
import time
from typing import Optional

# lib imports
import requests
from requests.cookies import RequestsCookieJar
import requests_cache
from requests_cache import CachedSession

# local imports
import plexhints
from plexhints import GLOBAL_DEFAULT_TIMEOUT

cookie_jar = RequestsCookieJar()
session = CachedSession()

# requests_cache.install_cache(cache_name='plexhints_cache', backend='memory')


def check_port(url):
    # type: (str) -> None
    """
    Check if the default port is in the URL

    Parameters
    ----------
    url : str
        The url to check.

    Raises
    ------
    Exception
        If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
        Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.
    """
    if ':32400/' in url and not plexhints.ELEVATED_POLICY:
        raise Exception("Accessing the media server's HTTP interface is not permitted.")


def http_request(url, values=None, headers=None, cache_time=None, encoding=None, errors=None,
                 timeout=GLOBAL_DEFAULT_TIMEOUT, immediate=False, sleep=0, data=None, opener=None,
                 follow_redirects=True, method=None):
    # type: (str, Optional[dict], Optional[dict], Optional[float], Optional[str], Optional[str], float, bool, float, Optional[str], Optional[any], bool, Optional[str]) -> requests.Response  # noqa: E501  # is it possible to have multiline type hints in python2?

    # todo - implement the following parameters:
    # encoding
    # errors
    # immediate
    # opener

    if method is None:
        method = 'GET'

    # sleep
    time.sleep(sleep)

    cache_option = requests_cache.enabled() if cache_time else session.cache_disabled()

    if cache_time:
        session._cache_expire_after = datetime.timedelta(seconds=cache_time)

    with cache_option:
        request_methods = dict(
            GET=session.get,
            POST=session.post,
            HEAD=session.head,
            DELETE=session.delete,
            PUT=session.put,
            OPTIONS=session.options
        )

    response = request_methods[method](url=url,
                                       data=values if values else data,
                                       headers=headers,
                                       timeout=timeout,
                                       allow_redirects=follow_redirects,
                                       )

    if cache_time:
        cookie_jar.set(name='plexhints_cache', value=response.cookies)

    return response

# future imports
from __future__ import absolute_import  # import like python 3

from future.moves.urllib.request import HTTPPasswordMgrWithDefaultRealm

# standard imports
import threading
from typing import Optional

# lib imports
from deprecation import deprecated
import requests
from requests.cookies import RequestsCookieJar

# local imports
from plexhints._helpers import check_port, cookie_jar, http_request
from plexhints import GLOBAL_DEFAULT_TIMEOUT
from plexhints.const import PLEX_FRAMEWORK_VERSION
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()

password_manager = HTTPPasswordMgrWithDefaultRealm()


class _HTTPKit:
    """
    The HTTP API provides methods for making HTTP requests and interacting with the framework's HTTP subsystem.
    """

    def __init__(self):
        self._cache_time = 0
        self._custom_headers = dict()
        self._default_timeout = 20

    @property
    def CacheTime(self):
        # type: () -> int
        """
        float
            The default cache time (in seconds) used for all HTTP requests without a specific cache time set. By
            default, this value is 0.
        """
        return self._cache_time

    @CacheTime.setter
    def CacheTime(self, value):
        # type: (int) -> None
        self._cache_time = value

    @property
    def Headers(self):
        """
        dict
            A dictionary containing the default HTTP headers that should be issued with requests::

                HTTP.Headers['User-Agent'] = 'My Plug-in'
        """
        return self._custom_headers

    @deprecated(deprecated_in=None, removed_in=None, current_version=PLEX_FRAMEWORK_VERSION,
                details='The HTTP.SetCacheTime() function is deprecated. Use the HTTP.CacheTime property instead.')
    def SetCacheTime(self, cacheTime):
        # type: (float) -> None
        _Log.Warn('The HTTP.SetCacheTime() function is deprecated. Use the HTTP.CacheTime property instead.')
        self._cache_time = cacheTime

    @deprecated(deprecated_in=None, removed_in=None, current_version=PLEX_FRAMEWORK_VERSION,
                details='The HTTP.SetHeader() function is deprecated. '
                        'Use HTTP.Headers[] to get and set headers instead.')
    def SetHeader(self, header, value):
        # type: (str, any) -> None
        _Log.Warn('The HTTP.SetHeader() function is deprecated. Use HTTP.Headers[] to get and set headers instead.')
        self.Headers[header] = value

    @deprecated(deprecated_in=None, removed_in=None, current_version=PLEX_FRAMEWORK_VERSION,
                details='The HTTP.SetTimeout() function is deprecated. Use the Network.Timeout property instead.')
    def SetTimeout(self, timeout):
        # type: (float) -> None
        _Log.Warn('The HTTP.SetTimeout() function is deprecated. Use the Network.Timeout property instead.')
        self._default_timeout = timeout

    def Request(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                timeout=GLOBAL_DEFAULT_TIMEOUT, immediate=False, sleep=0, data=None, follow_redirects=True,
                method=None):
        # type: (str, Optional[dict], dict, Optional[int], Optional[str], Optional[str], float, bool, float, Optional[str], bool, Optional[str]) -> requests.Response  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Creates and returns a new :class:`HTTPRequest` object.

        Parameters
        ----------
        url : str
            The URL to use for the request.
        values : Optional[dict]
            Keys and values to be URL encoded and provided as the request's POST body.
        headers : dict, default={}
            Any custom HTTP headers that should be added to this request.
        cacheTime : Optional[int]
            The maximum age (in second) of cached data before it should be considered invalid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) to wait for the request to return a response before timing out.
        immediate : bool, default=False
            If set to ``True``, the HTTP request will be made immediately when the object is created (by default,
            requests are delayed until the data they return is requested).
        sleep : float, default=0
            The amount of time (in seconds) that the current thread should be paused for after issuing an HTTP request.
            This is to ensure undue burden is not placed on the server. If the data is retrieved from the cache,
            this value is ignored.
        data : Optional[str]
            The raw POST data that should be sent with the request. This attribute cannot be used in conjunction with
            `values`.
        follow_redirects : bool, default=False
            Specifies whether redirects should be followed, or if an exception should be raised. If False, the
            framework will raise a RedirectError when encountering a redirected response.
        method : Optional[str]
            Supported methods: `GET`, `HEAD`, `POST`, `DELETE`, `PUT`, `OPTIONS`.

        Returns
        -------
        requests.Response
            The Response of the http request.
        """

        # Update the cache time
        self._cache_time = cacheTime if (values is None and data is None) else 0

        check_port(url=url)
        all_headers = headers

        return http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            immediate=immediate,
            sleep=sleep,
            data=data,
            opener=None,  # todo
            follow_redirects=follow_redirects,
            method=method,
        )

    def CookiesForURL(self, url):
        # type: (str) -> Optional[dict]
        """
        Returns the cookies associated with the given URL.

        Parameters
        ----------
        url : str
            The url to obtain cookies for.

        Returns
        -------
        dict
            Dictionary of cookies for the given url if there are cookies, otherwise ``None``.
        """
        response = requests.post(url=url)
        cookies = response.cookies

        return cookies if cookies else None

    @deprecated(deprecated_in=None, removed_in=None, current_version=PLEX_FRAMEWORK_VERSION,
                details='HTTP.GetCookiesForURL() is deprecated - please use HTTP.CookiesForURL() instead.')
    def GetCookiesForURL(self, url):
        # type: (str) -> Optional[dict]
        _Log.Warn("HTTP.GetCookiesForURL() is deprecated - please use HTTP.CookiesForURL() instead.")
        return self.CookiesForURL(url)

    def SetPassword(self, url, username, password, realm=None):
        # type: (str, str, str, Optional[str]) -> None
        return password_manager.add_password(realm=realm, uri=url, user=username, passwd=password)

    def PreCache(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str]) -> None
        """
        Instructs the framework to pre-cache the result of a given HTTP request in a background
        thread. This method returns nothing - it is designed to ensure that cached data is
        available for future calls to `HTTP.Request`.
        """
        threading.Thread(target=self.Request, kwargs=dict(url=url, values=values, headers=headers, cacheTime=cacheTime,
                                                          encoding=encoding, errors=errors))

    @property
    def Cookies(self):
        # type: () -> RequestsCookieJar
        """
        Returns an iterable object containing all cookies.
        """
        return cookie_jar

    def ClearCookies(self):
        # type: () -> None
        """
        Clears the plug-in's HTTP cookies.
        """
        cookie_jar.clear()

    def ClearCache(self):
        # type: () -> None
        """
        Clears the plug-in's HTTP cache.
        """
        pass

    @deprecated(deprecated_in=None, removed_in=None, current_version=PLEX_FRAMEWORK_VERSION,
                details='Randomized user agent strings are no longer supported.')
    def RandomizeUserAgent(self, browser=None):
        # type: (Optional[str]) -> None
        """
        Random user agents are not supported. This function should no longer be used.
        """
        _Log.Error("Randomized user agent strings are no longer supported.")


HTTP = _HTTPKit()

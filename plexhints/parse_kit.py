# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import plistlib
import sys
from typing import Optional

# lib imports
import feedparser
from bs4.dammit import UnicodeDammit
from lxml import etree, html, objectify
from lxml.html import soupparser, HTMLParser
import simplejson
import yaml

# local imports
from plexhints._helpers import check_port, http_request
from plexhints import GLOBAL_DEFAULT_TIMEOUT
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()

# conditional imports
if sys.version_info.major < 3:
    import demjson
else:
    import demjson3 as demjson


def check_size(data, max_size=5242880):
    # type: (str, int) -> None
    """
    Make sure we don't try to parse anything greater than the given maximum size.

    Parameters
    ----------
    data : str
        The data to check.
    max_size : int, default=5242880
        The maximum size in bytes.

    Raises
    ------
    Exception
        `Exception` in this library, `Framework.exceptions.APIException` in Plex Framework`
    """
    if max_size is not None and len(data) > max_size:
        raise Exception("Data of size %d is greater than the maximum size %d" % (len(data), max_size))


def json_from_string(json_string, encoding=None):
    # type: (str, Optional[str]) -> dict
    try:
        return simplejson.loads(json_string, encoding)
    except simplejson.scanner.JSONDecodeError as e:
        _Log.Warn("Error decoding with simplejson, using demjson instead (this will cause a performance hit)")
        _Log.Exception('JSON decoding error - %s' % e)
        return demjson.decode(json_string, encoding)


def json_to_string(obj):
    # type: (dict) -> str
    try:
        return simplejson.dumps(obj)
    except Exception:
        _Log.Warn("Error encoding with simplejson, trying demjson instead. This will cause a performance hit.")
        _Log.Exception('JSON encoding error')
        return demjson.encode(obj)


def html_element(name, text, **kwargs):
    # type: (str, str, **any) -> html.HtmlElement
    """
    Create an HTML element.

    Parameters
    ----------
    name : str
        The name of the element.
    text : str
        The text content of the element.
    **kwargs : **any
        Key word arguments.

    Returns
    -------
    etree.Element
        The element.
    """
    el = html.HtmlElement(name)

    if text:
        el.text = text
    for key in kwargs:
        el.set(key, kwargs[key])
    return el


def xml_element(name, text, **kwargs):
    # type: (str, str, **any) -> etree.Element
    """
    Create an XML element.

    Parameters
    ----------
    name : str
        The name of the element.
    text : str
        The text content of the element.
    **kwargs : **any
        Key word arguments.

    Returns
    -------
    etree.Element
        The element.
    """
    el = etree.Element(name)

    if text:
        el.text = text
    for key in kwargs:
        el.set(key, kwargs[key])
    return el


def xml_element_from_string(string, is_html=False, encoding=None, remove_blank_text=False):
    # type: (str, bool, Optional[str], bool ) -> etree.Element
    """
    Create an element from a string.

    Parameters
    ----------
    string : str
        The string to convert.
    is_html : bool
        Used for encoding special characters.
    encoding : str
        The encoding to use.
    remove_blank_text : bool
        Remove white space.

    Returns
    -------
    etree.Element
        The element.
    """
    if string is None:
        return None

    if encoding is None:
        ud = UnicodeDammit(str(string), is_html=is_html)
        markup = ud.markup.encode('utf-8')
    else:
        markup = str(string).encode(encoding)

    if is_html:
        try:
            return html.fromstring(markup, parser=HTMLParser(encoding='utf-8'))
        except Exception:
            _Log.Exception('Error parsing with lxml, falling back to soupparser')
            return soupparser.fromstring(string)
    else:
        return etree.fromstring(markup, parser=(etree.XMLParser(remove_blank_text=True) if remove_blank_text else None))


def xml_element_to_string(el, encoding='utf-8', method=None):
    # type: (etree.Element, str, Optional[str]) -> str
    """
    Convert an element to string.

    Parameters
    ----------
    el : etree.Element
        The element to convert.
    encoding : str, default='utf-8'
        The encoding to use.
    method : Optional[str]
        Accepted method types are ``html`` and ``xml``.

    Raises
    ------
    Exception
        If method type is not ``html`` or ``xml``. The original Plex Framework does not raise anything.

    Returns
    -------
    str
        The converted element as a string.
    """
    if method is None:
        if isinstance(el, html.HtmlElement):
            method = 'html'
        else:
            method = 'xml'

    if method == 'xml':
        return etree.tostring(el, pretty_print=True, encoding=encoding, xml_declaration=True).decode(encoding)
    elif method == 'html':
        return html.tostring(el, method=method, encoding=encoding).decode(encoding)

    if method != 'xml' or method != 'html':
        raise Exception('%s is not an allowed method, use "html" or "xml" only.' % method)


def xml_object_from_string(string):
    # type: (str) -> objectify.Element
    return objectify.fromstring(xml=string)


def xml_object_to_string(obj, encoding='utf-8'):
    # type: (objectify.ObjectifiedElement, str) -> etree.Element
    return etree.tostring(obj, pretty_print=True, encoding=encoding).decode(encoding)


class _HTMLKit:
    """
    The HTML API is similar to the XML API, but is better suited to parsing HTML content. It is powered by the lxml
    `html <https://lxml.de/lxmlhtml.html>`_ library.
    """
    def __init__(self):
        pass

    def Element(self, name, text=None, **kwargs):
        # type: (str, Optional[str], **any) -> html.HtmlElement
        """
        Returns a new HTML element with the given name and text content. Any keyword arguments provided will be set as
        attributes.

        Parameters
        ----------
        name : str
            The name of the new element.
        text : Optional[str]
            The text content of the new element.
        **kwargs : **any
            Keyword arguments of attributes to set.

        Returns
        -------
        html.HtmlElement
            An `html.HtmlElement <https://lxml.de/lxmlhtml.html#html-element-methods>`_ object.
        """
        return html_element(name=name, text=text, **kwargs)

    def StringFromElement(self, el, encoding='utf8'):
        # type: (html.HtmlElement, str) -> str
        """
        Converts the HTML element object `el` to a string representation using the given encoding.

        Parameters
        ----------
        el : html.HtmlElement
            The HTML element to convert.
        encoding : str, default='utf-8'
            The string encoding.

        Returns
        -------
        str
            The converted string.
        """
        return xml_element_to_string(el=el, encoding=encoding, method='html')

    def ElementFromString(self, string, max_size=None):
        # type: (str, Optional[int]) -> html.HtmlElement
        """
        Converts `string` to an HTML element object.

        Parameters
        ----------
        string : str
            The string to convert.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Returns
        -------
        html.HtmlElement
            An `html.HtmlElement <https://lxml.de/lxmlhtml.html#html-element-methods>`_ object.
        """
        check_size(data=string, max_size=max_size)
        return xml_element_from_string(string, is_html=True)

    def ElementFromURL(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                       timeout=GLOBAL_DEFAULT_TIMEOUT, sleep=0, follow_redirects=True, method=None, max_size=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str], float, float, bool, Optional[str], Optional[int]) -> html.HtmlElement  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Retrieves the content for a given HTTP request and parses it as HTML using the above method.

        Parameters
        ----------
        url : str
            The URL to retrieve content from.
        values : Optional[dict]
            Values to pass as URL encoded content for a POST request.
        headers : dict, default={}
            Custom HTTP headers to add to the request.
        cacheTime : Optional[float]
            The maximum age (in seconds) that cached data should still be considered valid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) that the framework should wait for a response before aborting.
        sleep : float, default=0
            The number of seconds the current thread should pause for if a network request was made, ensuring undue
            burden isn't placed on web servers. If cached data was used, this value is ignored.
        follow_redirects : bool, default=True
            Specifies whether redirects should be followed, or if an exception should be raised. If False, the
            framework will raise a RedirectError when encountering a redirected response.
        method : Optional[str]
            Supported methods: `GET`, `HEAD`, `POST`, `DELETE`, `PUT`, `OPTIONS`.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Raises
        ------
        Exception
            If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
            Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.

        Returns
        -------
        html.HtmlElement
            An `html.HtmlElement <https://lxml.de/lxmlhtml.html#html-element-methods>`_ object.
        """
        check_port(url=url)

        all_headers = headers
        return self.ElementFromString(http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            sleep=sleep,
            opener=None,  # todo
            follow_redirects=follow_redirects,
            method=method,
        ).text, max_size=max_size)


class _JSONKit:
    """
    The JSON API provides methods for easily converting JSON-formatted strings into Python objects, and vice versa.

    More information about the JSON format can be found `here <https://www.json.org>`_.

    .. Note:: The framework includes two JSON parsers - one is fast, but very strict, while the second is slower but
       more tolerant of errors. If a string is unable to be parsed by the fast parser, an error will be logged
       indicating the position in the string where parsing failed. If possible, the developer should check for and
       resolve these errors, as slow JSON parsing can have a severely detrimental effect on performance, especially
       on embedded systems.
    """

    def ObjectFromString(self, string, encoding=None, max_size=None):
        # type: (str, Optional[str], Optional[int]) -> dict
        """
        Converts a JSON-formatted string into a Python object, usually a dictionary.

        Parameters
        ----------
        string : str
            The string to convert.
        encoding : Optional[str]
            The encoding to use. e.g. ``utf-8``.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Returns
        -------
        dict
            Dictionary object.
        """
        check_size(data=string, max_size=max_size)
        return json_from_string(json_string=string, encoding=encoding)

    def ObjectFromURL(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                      timeout=GLOBAL_DEFAULT_TIMEOUT, sleep=0, follow_redirects=True, method=None, max_size=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str], float, float, bool, Optional[str], Optional[int]) -> dict  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Retrieves the content for a given HTTP request and parses it as JSON-formatted content using the above method.

        Parameters
        ----------
        url : str
            The URL to retrieve content from.
        values : Optional[dict]
            Values to pass as URL encoded content for a POST request.
        headers : dict, default={}
            Custom HTTP headers to add to the request.
        cacheTime : Optional[float]
            The maximum age (in seconds) that cached data should still be considered valid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) that the framework should wait for a response before aborting.
        sleep : float, default=0
            The number of seconds the current thread should pause for if a network request was made, ensuring undue
            burden isn't placed on web servers. If cached data was used, this value is ignored.
        follow_redirects : bool, default=True
            Specifies whether redirects should be followed, or if an exception should be raised. If False, the
            framework will raise a RedirectError when encountering a redirected response.
        method : Optional[str]
            Supported methods: `GET`, `HEAD`, `POST`, `DELETE`, `PUT`, `OPTIONS`.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Raises
        ------
        Exception
            If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
            Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.

        Returns
        -------
        dict
            Dictionary object.
        """
        check_port(url=url)

        all_headers = {'Accept': 'text/*, application/json'}
        all_headers.update(headers)

        return self.ObjectFromString(http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            sleep=sleep,
            opener=None,  # todo
            follow_redirects=follow_redirects,
            method=method,
        ).content, encoding, max_size=max_size)

    def StringFromObject(self, obj):
        # type: (dict) -> str
        """
        Converts the given object to a JSON-formatted string representation.

        Parameters
        ----------
        obj : dict
            Dictionary object to convert.

        Returns
        -------
        str
            The converted dictionary, formatted as a string.
        """
        return json_to_string(obj)


class _PlistKit:
    """
    The Plist API greatly simplifies handling content in Apple's XML-based property list format. Using these methods,
    data can easily be converted between property lists and regular Python objects. The top-level object of a property
    list is usually a dictionary.

    More information about the property list format can be found `here
    <https://web.archive.org/web/20150419011159/https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man5/plist.5.html>`_.
    """

    def __init__(self):
        pass

    def ObjectFromString(self, string, max_size=None):
        # type: (str, Optional[int]) -> dict
        """
        Returns an object representing the given Plist-formatted string.

        Parameters
        ----------
        string : str
            The Plist formatted as a string.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Returns
        -------
        dict
            An object representing the Plist.
        """
        check_size(data=string, max_size=max_size)
        try:
            return plistlib.readPlistFromString(string)
        except AttributeError:
            # python 3.x
            try:
                return plistlib.loads(string.encode('utf-8'))
            except AttributeError:
                # if string is already bytes
                return plistlib.loads(string)

    def ObjectFromURL(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                      timeout=GLOBAL_DEFAULT_TIMEOUT, sleep=0, follow_redirects=True, method=None, max_size=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str], float, float, bool, Optional[str], Optional[int]) -> dict  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Retrieves the content for a given HTTP request and parses it as a Plist using the above method.

        Parameters
        ----------
        url : str
            The URL to retrieve content from.
        values : Optional[dict]
            Values to pass as URL encoded content for a POST request.
        headers : dict, default={}
            Custom HTTP headers to add to the request.
        cacheTime : Optional[float]
            The maximum age (in seconds) that cached data should still be considered valid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) that the framework should wait for a response before aborting.
        sleep : float, default=0
            The number of seconds the current thread should pause for if a network request was made, ensuring undue
            burden isn't placed on web servers. If cached data was used, this value is ignored.
        follow_redirects : bool, default=True
            Specifies whether redirects should be followed, or if an exception should be raised. If False, the
            framework will raise a RedirectError when encountering a redirected response.
        method : Optional[str]
            Supported methods: `GET`, `HEAD`, `POST`, `DELETE`, `PUT`, `OPTIONS`.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Raises
        ------
        Exception
            If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
            Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.

        Returns
        -------
        dict
            Dictionary representation of url content.
        """
        check_port(url=url)

        all_headers = headers
        return self.ObjectFromString(http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            sleep=sleep,
            opener=None,  # todo
            follow_redirects=follow_redirects,
            method=method,
        ).content, max_size=max_size)

    def StringFromObject(self, obj):
        # type: (dict) -> str
        """
        Converts a given object to a Plist-formatted string representation.

        Parameters
        ----------
        obj : dict
            A Plist represented as a dictionary object.

        Returns
        -------
        str
            A Plist represented as a string.
        """
        try:
            return plistlib.writePlistToString(obj)
        except AttributeError:
            # python 3.x
            return plistlib.dumps(obj).decode('utf-8')


class _RSSKit:
    """
    The RSS API provides methods for parsing content from RSS, RDF and ATOM feeds. The framework includes the excellent
    Universal Feed Parser library to achieve this functionality.

    For more information about the objects returned by the feed parser, please consult the
    documentation <https://feedparser.readthedocs.io/en/latest/index.html>`_ here.
    """
    def __init__(self):
        pass

    def FeedFromString(self, string, max_size=None):
        # type: (str, Optional[int]) -> feedparser.FeedParserDict
        """
        Parses the given string as an RSS, RDF or ATOM feed (automatically detected).

        Parameters
        ----------
        string : str
            The RSS feed formatted as a string.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Returns
        -------
        feedparser.FeedParserDict
            The RSS string as a dictionary object.
        """
        check_size(data=string, max_size=max_size)
        return feedparser.parse(string)

    def FeedFromURL(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                    timeout=GLOBAL_DEFAULT_TIMEOUT, sleep=0, follow_redirects=True, method=None, max_size=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str], float, float, bool, Optional[str], Optional[int]) -> feedparser.FeedParserDict  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Retrieves the content for a given HTTP request and parses it as an RSS, RDF or ATOM feed using the above method.

        Parameters
        ----------
        url : str
            The URL to retrieve content from.
        values : Optional[dict]
            Values to pass as URL encoded content for a POST request.
        headers : dict, default={}
            Custom HTTP headers to add to the request.
        cacheTime : Optional[float]
            The maximum age (in seconds) that cached data should still be considered valid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) that the framework should wait for a response before aborting.
        sleep : float, default=0
            The number of seconds the current thread should pause for if a network request was made, ensuring undue
            burden isn't placed on web servers. If cached data was used, this value is ignored.
        follow_redirects : bool, default=True
            Specifies whether redirects should be followed, or if an exception should be raised. If False, the
            framework will raise a RedirectError when encountering a redirected response.
        method : Optional[str]
            Supported methods: `GET`, `HEAD`, `POST`, `DELETE`, `PUT`, `OPTIONS`.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Raises
        ------
        Exception
            If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
            Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.

        Returns
        -------
        feedparser.FeedParserDict
            The RSS url as a dictionary object.
        """
        check_port(url=url)

        all_headers = headers
        return self.FeedFromString(http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            sleep=sleep,
            opener=None,  # todo
            follow_redirects=follow_redirects,
            method=method,
        ).content, max_size=max_size)


class _XMLKit:
    """
    The XML API provides methods for converting between XML-formatted strings and trees of XML Element objects. New
    XML element trees can also be constructed. The underlying functionality is provided by the lxml
    `etree <https://lxml.de/tutorial.html>`_ and `objectify <https://lxml.de/objectify.html>`_
    libraries.

    .. Note:: It is strongly recommended that developers read lxml's
       `XPath Tutorial <https://lxml.de/xpathxslt.html>`_. Manipulating elements returned by the etree library using
       XPath is a very powerful way of finding and accessing data within a XML document. Learning to use XPath
       efficiently will greatly simplify the plug-in's code.

    Methods
    -------
    Element:
        See below.
    StringFromElement:
        See below.
    ElementFromString:
        See below.
    ElementFromURL:
        See below.
    ObjectFromString:
        See below.
    StringFromObject:
        See below.
    ObjectFromURL:
        See below.
    """

    def __init__(self):
        pass

    def Element(self, name, text=None, **kwargs):
        # type: (str, Optional[str], **any) -> etree.Element
        """
        Returns a new XML element with the given name and text content. Any keyword arguments provided will be set as
        attributes.

        Parameters
        ----------
        name : str
            The name of the new element.
        text : str
            The text content of the new element.
        **kwargs : **any
            Keyword arguments of attributes to set.

        Returns
        -------
        etree.Element
            An `etree.Element <https://lxml.de/tutorial.html#the-element-class>`_ object.
        """
        return xml_element(name=name, text=text, **kwargs)

    def StringFromElement(self, el, encoding='utf8'):
        # type: (etree.Element, str) -> str
        """
        Converts the XML element object `el` to a string representation using the given encoding.

        Parameters
        ----------
        el : etree.Element
            The XML element to convert.
        encoding : str, default='utf-8'
            The string encoding.

        Returns
        -------
        str
            The converted string.
        """
        return xml_element_to_string(el=el, encoding=encoding, method=None)

    def ElementFromString(self, string, encoding=None, max_size=None):
        # type: (str, Optional[str], Optional[int]) -> etree.Element
        """
        Converts `string` to an XML element object.

        Parameters
        ----------
        string : str
            The string to convert.
        encoding : Optional[str]
            The encoding to use. e.g. ``utf-8``.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Returns
        -------
        etree.Element
            The element.
        """
        check_size(data=string, max_size=max_size)

        return xml_element_from_string(string=string, encoding=encoding)

    def ElementFromURL(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                       timeout=GLOBAL_DEFAULT_TIMEOUT, sleep=0, follow_redirects=True, method=None, max_size=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str], float, float, bool, Optional[str], Optional[int]) -> etree.Element  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Retrieves the content for a given HTTP request and parses it as XML using the above method.

        Parameters
        ----------
        url : str
            The URL to retrieve content from.
        values : Optional[dict]
            Values to pass as URL encoded content for a POST request.
        headers : dict, default={}
            Custom HTTP headers to add to the request.
        cacheTime : Optional[float]
            The maximum age (in seconds) that cached data should still be considered valid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) that the framework should wait for a response before aborting.
        sleep : float, default=0
            The number of seconds the current thread should pause for if a network request was made, ensuring undue
            burden isn't placed on web servers. If cached data was used, this value is ignored.
        follow_redirects : bool, default=True
            Specifies whether redirects should be followed, or if an exception should be raised. If False,
            the framework will raise a RedirectError when encountering a redirected response.
        method : Optional[str]
            Supported methods: `GET`, `HEAD`, `POST`, `DELETE`, `PUT`, `OPTIONS`.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Raises
        ------
        Exception
            If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
            Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.

        Returns
        -------
        etree.Element
            The element.
        """
        check_port(url=url)

        all_headers = headers
        return self.ElementFromString(string=http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            sleep=sleep,
            opener=None,  # todo
            follow_redirects=follow_redirects,
            method=method,
        ).text, encoding=encoding, max_size=max_size)

    def ObjectFromString(self, string, max_size=None):
        # type: (str, Optional[int]) -> objectify.ObjectifiedElement
        """
        Parses `string` as XML-formatted content and attempts to build a Python object using the ``objectify`` library.

        Parameters
        ----------
        string : str
            The string to parse.
        max_size : Optional[int]
            The maximum size to allow, in bytes.

        Returns
        -------
        objectify.ObjectifiedElement
            `ObjectifiedElement <https://lxml.de/api/lxml.objectify.ObjectifiedElement-class.html>`_ of the
            ``lxml.objectify`` module.
        """
        check_size(data=string, max_size=max_size)
        return xml_object_from_string(string=string)

    def StringFromObject(self, obj, encoding='utf-8'):
        # type: (objectify.ObjectifiedElement, str) -> str
        """
        Attempts to create objectified XML from the given object.

        Parameters
        ----------
        obj : objectify.ObjectifiedElement
            The element.
        encoding : str, default='utf-8'
            The encoding to use.

        Returns
        -------
        str
            The converted string.
        """
        return xml_object_to_string(obj=obj, encoding=encoding)

    def ObjectFromURL(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                      timeout=GLOBAL_DEFAULT_TIMEOUT, sleep=0, max_size=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str], float, float, Optional[int]) -> objectify.ObjectifiedElement  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Retrieves the content for a given HTTP request and parses it as objectified XML using the above method.

        Parameters
        ----------
        url : str
            The URL to retrieve content from.
        values : Optional[dict]
            Values to pass as URL encoded content for a POST request.
        headers : dict, default={}
            Custom HTTP headers to add to the request.
        cacheTime : Optional[float]
            The maximum age (in seconds) that cached data should still be considered valid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) that the framework should wait for a response before aborting.
        sleep : float, default=0
            The number of seconds the current thread should pause for if a network request was made, ensuring undue
            burden isn't placed on web servers. If cached data was used, this value is ignored.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.
        follow_redirects : bool
            Specifies whether redirects should be followed, or if an exception should be raised. If False,
            the framework will raise a RedirectError when encountering a redirected response.

            .. Warning:: This is missing from the Plex Framework. Do not use!

        Raises
        ------
        Exception
            If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
            Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.

        Returns
        -------
        objectify.ObjectifiedElement
            `ObjectifiedElement <https://lxml.de/api/lxml.objectify.ObjectifiedElement-class.html>`_ of the
            ``lxml.objectify`` module.
        """
        check_port(url=url)

        all_headers = headers
        return self.ObjectFromString(http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            sleep=sleep,
            opener=None,  # todo
        ).content, max_size=max_size)


class _YAMLKit:
    def ObjectFromString(self, string, max_size=None):
        # type: (str, Optional[int]) -> dict
        """
        Parses the given YAML-formatted string and returns the object it represents.

        Parameters
        ----------
        string : str
            The string to convert.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Returns
        -------
        dict
            A dictionary representation of the YAML string.
        """
        check_size(data=string, max_size=max_size)
        obj = yaml.safe_load(string)  # changed from load method to safe_load to prevent execution of arbitrary code
        return obj

    def ObjectFromURL(self, url, values=None, headers={}, cacheTime=None, encoding=None, errors=None,
                      timeout=GLOBAL_DEFAULT_TIMEOUT, sleep=0, follow_redirects=True, method=None, max_size=None):
        # type: (str, Optional[dict], dict, Optional[float], Optional[str], Optional[str], float, float, bool, Optional[str], Optional[int]) -> dict  # noqa: E501  # is it possible to have multiline type hints in python2?
        """
        Retrieves the content for a given HTTP request and parses it as YAML-formatted content using the above method.

        url : str
            The URL to retrieve content from.
        values : Optional[dict]
            Values to pass as URL encoded content for a POST request.
        headers : dict, default={}
            Custom HTTP headers to add to the request.
        cacheTime : Optional[float]
            The maximum age (in seconds) that cached data should still be considered valid.
        encoding : Optional[str]
            The string encoding to use for the downloaded data. If no encoding is provided, the framework will attempt
            to guess the encoding.
        errors : Optional[str]
            The error handling method to use. If `errors` is `'strict'` (the default), a `ValueError` is raised on
            errors, while a value of `'ignore'` causes errors to be silently ignored, and a value of `'replace'`
            causes the official Unicode replacement character, U+FFFD, to be used to replace input characters which
            cannot be decoded.
        timeout : float, default=20
            The maximum amount of time (in seconds) that the framework should wait for a response before aborting.
        sleep : float, default=0
            The number of seconds the current thread should pause for if a network request was made, ensuring undue
            burden isn't placed on web servers. If cached data was used, this value is ignored.
        follow_redirects : bool, default=True
            Specifies whether redirects should be followed, or if an exception should be raised. If False, the
            framework will raise a RedirectError when encountering a redirected response.
        method : Optional[str]
            Accepted method types are ``html`` and ``xml``. If not supplied, the Framework will attempt to determine
            the method automatically.
        max_size : Optional[int]
            The maximum size, in bytes, to accept.

        Raises
        ------
        Exception
            If accessing a Plex server url and not using an elevated `PlexPluginCodePolicy` in the plist file.
            Plex Framework will raise ``Framework.exceptions.FrameworkException`` instead.

        Returns
        -------
        dict
            Dictionary representation of the YAML url content.
        """
        check_port(url=url)

        all_headers = headers
        return self.ObjectFromString(http_request(
            url=url,
            values=values,
            headers=all_headers,
            cache_time=cacheTime,
            encoding=encoding,
            errors=errors,
            timeout=timeout,
            sleep=sleep,
            opener=None,  # todo
            follow_redirects=follow_redirects,
            method=method,
        ).content, max_size=max_size)


HTML = _HTMLKit()
JSON = _JSONKit()
Plist = _PlistKit()
RSS = _RSSKit()
XML = _XMLKit()
YAML = _YAMLKit()

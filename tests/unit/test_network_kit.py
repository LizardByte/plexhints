# -*- coding: utf-8 -*-

# lib imports
import pytest
from requests.cookies import RequestsCookieJar

# local imports
from plexhints import network_kit


@pytest.fixture(scope='function')
def http_kit():
    return network_kit._HTTPKit()


@pytest.fixture(scope='function')
def password_manager():
    return network_kit.password_manager


def test_http_kit_cache_time(http_kit):
    assert isinstance(http_kit.CacheTime, int)


def test_http_kit_cache_time_setter(http_kit):
    http_kit.CacheTime = 10
    assert http_kit.CacheTime == 10


def test_http_kit_headers(http_kit):
    assert isinstance(http_kit.Headers, dict)


def test_http_kit_headers_setter(http_kit):
    http_kit.Headers['User-Agent'] = 'My Plug-in'
    assert http_kit.Headers['User-Agent'] == 'My Plug-in'


def test_request(http_kit):
    response = http_kit.Request(url='https://github.com/LizardByte/plexhints')
    assert response.status_code == 200


def test_cookies_for_url(http_kit):
    cookies = http_kit.CookiesForURL(url='https://github.com/LizardByte/plexhints')
    assert cookies


def test_set_password(http_kit, password_manager):
    username = 'username'
    password = 'password'
    uri = 'https://www.plex.tv'
    realm = 'test'
    http_kit.SetPassword(
        url=uri,
        username=username,
        password=password,
        realm=realm
    )
    find_password = password_manager.find_user_password(
        authuri=uri,
        realm=realm,
    )
    assert find_password == (username, password)


def test_pre_cache(http_kit):
    url = 'https://github.com/LizardByte'
    http_kit.PreCache(url=url, cacheTime=1000)

    # this function does not return anything


def test_cookies(http_kit):
    cookies = http_kit.Cookies
    assert isinstance(cookies, RequestsCookieJar)


def test_clear_cookies(http_kit):
    # put something in the cookie jar
    http_kit.Cookies.set('test', 'test')

    assert len(http_kit.Cookies) > 0
    http_kit.ClearCookies()
    assert len(http_kit.Cookies) == 0


def test_clear_cache(http_kit):
    # this function does nothing
    http_kit.ClearCache()


def test_set_cache_time_depreciated(http_kit, caplog):
    http_kit.SetCacheTime(cacheTime=10)
    assert http_kit.CacheTime == 10

    # ensure deprecation warning is logged
    assert 'The HTTP.SetCacheTime() function is deprecated.' in caplog.text


def test_set_header_depreciated(http_kit, caplog):
    http_kit.SetHeader(header='User-Agent', value='My Plug-in')
    assert http_kit.Headers['User-Agent'] == 'My Plug-in'

    # ensure deprecation warning is logged
    assert 'The HTTP.SetHeader() function is deprecated.' in caplog.text


def test_set_timeout_depreciated(http_kit, caplog):
    http_kit.SetTimeout(timeout=10.0)
    assert http_kit._default_timeout == 10

    # ensure deprecation warning is logged
    assert 'The HTTP.SetTimeout() function is deprecated.' in caplog.text


def test_get_cookies_for_url_depreciated(http_kit, caplog):
    cookies = http_kit.GetCookiesForURL(url='https://github.com/LizardByte/plexhints')
    assert cookies

    # ensure deprecation warning is logged
    assert 'HTTP.GetCookiesForURL() is deprecated' in caplog.text


def test_randomize_user_agent_depreciated(http_kit, caplog):
    http_kit.RandomizeUserAgent()
    assert 'Randomized user agent strings are no longer supported.' in caplog.text

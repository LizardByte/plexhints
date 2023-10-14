# -*- coding: utf-8 -*-

# lib imports
import pytest

# local imports
from plexhints import locale_kit


def test_country_codes():
    country_codes = locale_kit.CountryCodes()
    assert country_codes.US == 'United States'


def test_language():
    language = locale_kit.Language()
    assert language.English == 'en'


@pytest.fixture(scope='function')
def locale():
    return locale_kit._LocaleKit()


def test_locale_kit_init(locale):
    assert locale.CountryCodes
    assert locale.Language
    assert locale._default_locale == 'en-us'


def test_locale_kit_default_locale(locale):
    assert locale.DefaultLocale == 'en-us'


def test_locale_kit_default_locale_setter(locale):
    locale.DefaultLocale = 'en-gb'
    assert locale.DefaultLocale == 'en-gb'


def test_locale_kit_geolocation(locale):
    assert locale.Geolocation == 'US'


def test_locale_kit_currernt_locale(locale):
    assert locale.CurrentLocale is None


def test_locale_kit_local_string(locale):
    assert locale.LocalString('test') == ''


def test_locale_kit_local_string_with_format(locale):
    assert locale.LocalStringWithFormat('test', 'format') == ''

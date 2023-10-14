# -*- coding: utf-8 -*-

# standard imports
import os

# lib imports
import pytest

# local imports
from plexhints import prefs_kit


@pytest.fixture(scope="function")
def text_pref():
    return prefs_kit._TextPref(
        label="foo",
        default_value="bar",
    )


def test_text_pref(text_pref):
    assert text_pref.type == 'text'
    assert text_pref.label == "foo"
    assert text_pref.default_value == "bar"
    assert text_pref.secure is False
    assert text_pref.hidden is False


def test_text_pref_encode_value(text_pref):
    assert text_pref.encode_value(encoded_value=None) == ""
    assert text_pref.encode_value(encoded_value="baz") == "baz"
    assert text_pref.encode_value(encoded_value=123) == "123"
    assert text_pref.encode_value(encoded_value=True) == "True"
    assert text_pref.encode_value(encoded_value=[1, 2, 3]) == "[1, 2, 3]"


def test_text_pref_decode_value(text_pref):
    assert text_pref.decode_value(value=None) is None
    assert text_pref.decode_value(value=[]) is None
    assert text_pref.decode_value(value="baz") == "baz"
    assert text_pref.decode_value(value=[1, 2, 3]) == "[1, 2, 3]"


def test_text_pref_info_dict(text_pref):
    info_dict = text_pref.info_dict(
        locale='en',
        value='foo',
        kw_arg='bar',
    )
    assert info_dict['type'] == 'text'
    assert info_dict['label'] == 'foo'
    assert info_dict['secure'] == 'false'
    assert info_dict['value'] == 'foo'
    assert info_dict['kw_arg'] == 'bar'


@pytest.fixture(scope="function")
def boolean_pref():
    return prefs_kit._BooleanPref(
        label="foo",
        default_value='true',
    )


def test_boolean_pref(boolean_pref):
    assert boolean_pref.type == 'bool'
    assert boolean_pref.label == "foo"
    assert boolean_pref.default_value == 'true'
    assert boolean_pref.secure is False
    assert boolean_pref.hidden is False


def test_boolean_encode_value(boolean_pref):
    assert boolean_pref.encode_value(value=True) == 'true'
    assert boolean_pref.encode_value(value='True') == 'true'
    assert boolean_pref.encode_value(value='true') == 'true'
    assert boolean_pref.encode_value(value=False) == 'false'
    assert boolean_pref.encode_value(value='False') == 'false'
    assert boolean_pref.encode_value(value='false') == 'false'
    assert boolean_pref.encode_value(value='123') == 'false'


def test_boolean_decode_value(boolean_pref):
    assert boolean_pref.decode_value(encoded_value=True) is True
    assert boolean_pref.decode_value(encoded_value='True') is True
    assert boolean_pref.decode_value(encoded_value='true') is True
    assert boolean_pref.decode_value(encoded_value=False) is False
    assert boolean_pref.decode_value(encoded_value='False') is False
    assert boolean_pref.decode_value(encoded_value='false') is False
    assert boolean_pref.decode_value(encoded_value='123') is False


@pytest.fixture(scope="function")
def enum_pref():
    return prefs_kit._EnumPref(
        label="foo",
        default_value='bar',
        values=['bar', 'baz', 'qux'],
    )


def test_enum_pref(enum_pref):
    assert enum_pref.type == 'enum'
    assert enum_pref.label == "foo"
    assert enum_pref.default_value == str(enum_pref.values.index('bar'))
    assert enum_pref.values == ['bar', 'baz', 'qux']
    assert enum_pref.secure is False
    assert enum_pref.hidden is False


def test_enum_pref_encode_value(enum_pref):
    assert enum_pref.encode_value(value='bar') == '0'
    assert enum_pref.encode_value(value='baz') == '1'
    assert enum_pref.encode_value(value='qux') == '2'
    assert enum_pref.encode_value(value='quux') is None


def test_enum_pref_decode_value(enum_pref):
    assert enum_pref.decode_value(encoded_value=0) == 'bar'
    assert enum_pref.decode_value(encoded_value='0') == 'bar'
    assert enum_pref.decode_value(encoded_value=1) == 'baz'
    assert enum_pref.decode_value(encoded_value='1') == 'baz'
    assert enum_pref.decode_value(encoded_value=2) == 'qux'
    assert enum_pref.decode_value(encoded_value='2') == 'qux'
    assert enum_pref.decode_value(encoded_value=3) is None
    assert enum_pref.decode_value(encoded_value='3') is None


def test_enum_pref_info_dict(enum_pref):
    info_dict = enum_pref.info_dict(
        locale='en',
        value='bar',
    )
    assert info_dict['type'] == 'enum'
    assert info_dict['label'] == 'foo'
    assert info_dict['secure'] == 'false'
    assert info_dict['value'] == '0'
    assert info_dict['values'] == 'bar|baz|qux'


@pytest.fixture(scope="function")
def preference_set():
    return prefs_kit._PreferenceSet(identifier='dev.lizardbyte.plexhints-test')


def test_preference_set_user_file_path(preference_set):
    assert preference_set._user_file_path.endswith('dev.lizardbyte.plexhints-test.xml')


def test_preference_set_load_user_file(preference_set):
    assert preference_set._user_values_dict == {}


def test_preference_set_save_user_file(preference_set):
    preference_set._save_user_file()
    assert os.path.isfile(preference_set._user_file_path)

    # remove the file
    os.remove(preference_set._user_file_path)


def test_preference_set_user_values(preference_set):
    assert preference_set._user_values == {}


def test_preference_set_update_user_values(preference_set):
    preference_set.update_user_values(pref1='foo', pref2='bar', pref3=True, pref4='bar')
    assert preference_set._user_values['pref1'] == 'foo'
    assert preference_set._user_values['pref2'] == 'bar'
    assert preference_set._user_values['pref3'] == 'true'
    assert preference_set._user_values['pref4'] == 'bar'


def test_preference_set_prefs(preference_set):
    assert isinstance(preference_set._prefs['pref1'], prefs_kit._TextPref)
    assert isinstance(preference_set._prefs['pref2'], prefs_kit._TextPref)
    assert isinstance(preference_set._prefs['pref3'], prefs_kit._BooleanPref)
    assert isinstance(preference_set._prefs['pref4'], prefs_kit._EnumPref)


def test_preference_set_default_prefs_path(preference_set):
    assert 'Contents' in preference_set.default_prefs_path
    assert preference_set.default_prefs_path.endswith('DefaultPrefs.json')


def test_preference_set_load_prefs(preference_set):
    preference_set._load_prefs()
    assert preference_set._prefs['pref1'].label == 'Text preference'
    assert preference_set._prefs['pref1'].default_value == 'Default Value'
    assert preference_set._prefs['pref1'].type == 'text'

    assert preference_set._prefs['pref2'].label == 'Hidden text preference (passwords, etc.)'
    assert preference_set._prefs['pref2'].default_value == ''
    assert preference_set._prefs['pref2'].type == 'text'
    assert preference_set._prefs['pref2'].secure is True
    assert preference_set._prefs['pref2'].options == ['hidden']

    assert preference_set._prefs['pref3'].label == 'Boolean preference'
    assert preference_set._prefs['pref3'].default_value == 'true'
    assert preference_set._prefs['pref3'].type == 'bool'

    assert preference_set._prefs['pref4'].label == 'Enum preference'
    assert preference_set._prefs['pref4'].default_value == '2'  # third item in the list
    assert preference_set._prefs['pref4'].type == 'enum'
    assert preference_set._prefs['pref4'].values == ['value1', 'value2', 'value3']

    assert preference_set._prefs['pref1-b'].label == 'Text preference'
    assert preference_set._prefs['pref1-b'].hidden is True


def test_preference_set_getitem(preference_set):
    assert preference_set['pref1'] == 'Default Value'
    assert preference_set['pref2'] is None
    assert preference_set['pref3'] is True
    assert preference_set['pref4'] == 'value3'

    with pytest.raises(KeyError):
        test = preference_set['pref5']
        assert test is None

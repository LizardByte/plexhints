# -*- coding: utf-8 -*-

# standard imports
import os
import sys

# lib imports
import pytest

# conditional imports
if sys.version_info.major < 3:
    import demjson
else:
    import demjson3 as demjson

# local imports
from plexhints import parse_kit


def test_check_size():
    two_bytes = b'\x00\x00'
    parse_kit.check_size(data=two_bytes, max_size=2)

    parse_kit.check_size(data=two_bytes, max_size=3)

    with pytest.raises(Exception):
        parse_kit.check_size(data=two_bytes, max_size=1)


def test_json_from_string():
    json_string = '{"foo": "bar"}'
    json_data = parse_kit.json_from_string(json_string=json_string)
    assert json_data['foo'] == 'bar'

    with pytest.raises(demjson.JSONDecodeError):
        parse_kit.json_from_string(json_string='')


def test_json_to_string():
    obj = {'foo': 'bar'}
    json_string = parse_kit.json_to_string(obj=obj)
    assert json_string == '{"foo": "bar"}'

    # force an encoding error
    with pytest.raises(demjson.JSONEncodeError):
        parse_kit.json_to_string(obj=object())


def test_html_element():
    name = 'foo'
    text = 'bar'
    element = parse_kit.html_element(name=name, text=text, key1='value1', key2='value2')
    assert element.text == text
    assert element.get('key1') == 'value1'
    assert element.get('key2') == 'value2'


def test_xml_element():
    name = 'foo'
    text = 'bar'
    element = parse_kit.xml_element(name=name, text=text, key1='value1', key2='value2')
    assert element.text == text
    assert element.get('key1') == 'value1'
    assert element.get('key2') == 'value2'


def test_xml_element_from_string():
    xml_string = '<foo>bar</foo>'
    element = parse_kit.xml_element_from_string(string=xml_string)
    assert element.text == 'bar'

    # nested xml
    xml_string = """
    <foo>
        <bar>baz</bar>
        <car>caz</car>
    </foo>
    """
    element = parse_kit.xml_element_from_string(string=xml_string)
    assert element.find('bar').text == 'baz'
    assert element.find('car').text == 'caz'


def test_xml_element_from_string_html():
    html_string = '<foo>bar</foo>'
    element = parse_kit.xml_element_from_string(string=html_string, is_html=True)
    assert element.text == 'bar'

    # nested html
    html_string = """
    <foo>
        <bar>baz</bar>
        <car>caz</car>
    </foo>
    """
    element = parse_kit.xml_element_from_string(string=html_string, is_html=True)
    assert element.find('bar').text == 'baz'
    assert element.find('car').text == 'caz'


def test_xml_element_to_string():
    element = parse_kit.xml_element(name='foo', text='bar')
    xml_string = parse_kit.xml_element_to_string(el=element, method=None)
    assert '<foo>bar</foo>' in xml_string

    xml_string = parse_kit.xml_element_to_string(el=element, method='html')
    assert '<foo>bar</foo>' in xml_string

    xml_string = parse_kit.xml_element_to_string(el=element, method='xml')
    assert '<foo>bar</foo>' in xml_string


def test_xml_object_from_string():
    xml_string = '<foo>bar</foo>'
    xml_object = parse_kit.xml_object_from_string(string=xml_string)
    assert xml_object.text == 'bar'

    # nested xml
    xml_string = """
    <foo>
        <bar>baz</bar>
        <car>caz</car>
    </foo>
    """
    xml_object = parse_kit.xml_object_from_string(string=xml_string)
    assert xml_object.find('bar').text == 'baz'
    assert xml_object.find('car').text == 'caz'


def test_xml_object_to_string():
    og_xml_string = '<foo>bar</foo>'
    xml_object = parse_kit.xml_object_from_string(string=og_xml_string)
    xml_string = parse_kit.xml_object_to_string(obj=xml_object)
    assert xml_string.replace(r'\n', '').strip() == og_xml_string

    # nested xml
    og_xml_string = """<foo>
  <bar>baz</bar>
  <car>caz</car>
</foo>
"""
    xml_object = parse_kit.xml_object_from_string(string=og_xml_string)
    xml_string = parse_kit.xml_object_to_string(obj=xml_object)
    assert xml_string.strip() == og_xml_string.strip()


@pytest.fixture(scope='module')
def html_kit():
    return parse_kit._HTMLKit()


def test_html_kit_element(html_kit):
    name = 'foo'
    text = 'bar'
    element = html_kit.Element(name=name, text=text, key1='value1', key2='value2')
    assert element.text == text
    assert element.get('key1') == 'value1'
    assert element.get('key2') == 'value2'


def test_html_kit_string_from_element(html_kit):
    html_element = parse_kit.xml_element_from_string(string='<foo>bar</foo>', is_html=True)
    html_string = html_kit.StringFromElement(el=html_element)
    assert html_string == '<foo>bar</foo>'


def test_html_kit_element_from_string(html_kit):
    html_string = '<foo>bar</foo>'
    html_element = html_kit.ElementFromString(string=html_string)
    assert html_element.text == 'bar'

    # nested html
    html_string = """
    <foo>
        <bar>baz</bar>
        <car>caz</car>
    </foo>
    """
    html_element = html_kit.ElementFromString(string=html_string)
    assert html_element.find('bar').text == 'baz'
    assert html_element.find('car').text == 'caz'


def test_html_kit_element_from_url(html_kit, http_server):
    dummy_file = 'dummy-data.html'
    html_element = html_kit.ElementFromURL(url=http_server.format(dummy_file))
    assert html_element.tag == 'html'
    assert html_element.find('body').find('h1').text == 'My First Heading'
    assert html_element.find('body').find('p').text == 'My first paragraph.'


@pytest.fixture(scope='module')
def json_kit():
    return parse_kit._JSONKit()


def test_json_kit_object_from_string(json_kit):
    json_string = '{"foo": "bar"}'
    json_object = json_kit.ObjectFromString(string=json_string)
    assert json_object['foo'] == 'bar'


def test_json_kit_object_from_url(http_server, json_kit):
    dummy_file = 'dummy-data.json'
    json_object = json_kit.ObjectFromURL(url=http_server.format(dummy_file))
    assert json_object[0]['name'] == 'Adeel Solangi'
    assert json_object[1]['version'] == 1.88


def test_json_kit_string_from_object(json_kit):
    json_object = {'foo': 'bar'}
    json_string = json_kit.StringFromObject(obj=json_object)
    assert json_string == '{"foo": "bar"}'


@pytest.fixture(scope='module')
def plist_kit():
    return parse_kit._PlistKit()


def test_plist_kit_object_from_string(plist_kit):
    plist_string = '<plist><dict><key>foo</key><string>bar</string></dict></plist>'
    plist_object = plist_kit.ObjectFromString(string=plist_string)
    assert plist_object['foo'] == 'bar'


def test_plist_kit_object_from_url(http_server, plist_kit):
    dummy_file = 'dummy-data.plist'

    plist_object = plist_kit.ObjectFromURL(url=http_server.format(dummy_file))
    assert plist_object['CFBundleDevelopmentRegion'] == 'English'


def test_plist_kit_string_from_object(plist_kit):
    plist_object = {'foo': 'bar'}
    plist_string = plist_kit.StringFromObject(obj=plist_object)
    assert '<key>foo</key>' in plist_string
    assert '<string>bar</string>' in plist_string


@pytest.fixture(scope='module')
def rss_kit():
    return parse_kit._RSSKit()


def test_rss_kit_feed_from_string(rss_kit):
    # open dummy file
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dummy-data.rss'), 'r') as f:
        rss_string = f.read()

    rss_feed = rss_kit.FeedFromString(string=rss_string)
    assert rss_feed['channel']['title'] == 'W3Schools Home Page'


def test_rss_kit_feed_from_url(http_server, rss_kit):
    dummy_file = 'dummy-data.rss'
    rss_feed = rss_kit.FeedFromURL(url=http_server.format(dummy_file))
    assert rss_feed['channel']['title'] == 'W3Schools Home Page'


@pytest.fixture(scope='module')
def xml_kit():
    return parse_kit._XMLKit()


def test_xml_kit_element(xml_kit):
    name = 'foo'
    text = 'bar'
    element = xml_kit.Element(name=name, text=text, key1='value1', key2='value2')
    assert element.text == text
    assert element.get('key1') == 'value1'
    assert element.get('key2') == 'value2'


def test_xml_kit_string_from_element(xml_kit):
    xml_element = parse_kit.xml_element_from_string(string='<foo>bar</foo>')
    xml_string = xml_kit.StringFromElement(el=xml_element)
    assert '<foo>bar</foo>' in xml_string


def test_xml_kit_element_from_string(xml_kit):
    xml_string = '<foo>bar</foo>'
    xml_element = xml_kit.ElementFromString(string=xml_string)
    assert xml_element.text == 'bar'

    # nested xml
    xml_string = """
    <foo>
        <bar>baz</bar>
        <car>caz</car>
    </foo>
    """
    xml_element = xml_kit.ElementFromString(string=xml_string)
    assert xml_element.find('bar').text == 'baz'
    assert xml_element.find('car').text == 'caz'


def test_xml_kit_element_from_url(http_server, xml_kit):
    dummy_file = 'dummy-data.xml'
    xml_element = xml_kit.ElementFromURL(url=http_server.format(dummy_file))
    assert xml_element.tag == 'catalog'
    assert xml_element.find('book').find('author').text == 'Gambardella, Matthew'

    # second book
    assert xml_element.find('book[2]').find('author').text == 'Ralls, Kim'
    assert xml_element.find('book[2]').find('title').text == 'Midnight Rain'


def test_xml_kit_object_from_string(xml_kit):
    # read dummy file
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dummy-data.xml'), 'r') as f:
        xml_string = f.read()

    xml_object = xml_kit.ObjectFromString(string=xml_string)
    assert xml_object.find('book').find('author').text == 'Gambardella, Matthew'

    # second book
    assert xml_object.find('book[2]').find('author').text == 'Ralls, Kim'


def test_xml_kit_string_from_object(xml_kit):
    xml_object = parse_kit.xml_element_from_string(string='<foo>bar</foo>')
    xml_string = xml_kit.StringFromObject(obj=xml_object)
    assert xml_string.replace(r'\n', '').strip() == '<foo>bar</foo>'


def test_xml_kit_object_from_url(http_server, xml_kit):
    dummy_file = 'dummy-data.xml'
    xml_object = xml_kit.ObjectFromURL(url=http_server.format(dummy_file))
    assert xml_object.find('book').find('author').text == 'Gambardella, Matthew'

    # second book
    assert xml_object.find('book[2]').find('author').text == 'Ralls, Kim'


@pytest.fixture(scope='module')
def yaml_kit():
    return parse_kit._YAMLKit()


def test_yaml_kit_object_from_string(yaml_kit):
    # open dummy file
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dummy-data.yml'), 'r') as f:
        yaml_string = f.read()

    yaml_object = yaml_kit.ObjectFromString(string=yaml_string)
    assert yaml_object['info']['name'] == 'John Doe'
    assert yaml_object['info']['age'] == 30
    assert 'English' in yaml_object['languages']


def test_yaml_kit_object_from_url(http_server, yaml_kit):
    dummy_file = 'dummy-data.yml'
    yaml_object = yaml_kit.ObjectFromURL(url=http_server.format(dummy_file))
    assert yaml_object['info']['name'] == 'John Doe'
    assert yaml_object['info']['age'] == 30
    assert 'English' in yaml_object['languages']

# -*- coding: utf-8 -*-

# standard imports
from future.moves.urllib.parse import quote

# lib imports
import pytest

# local imports
from plexhints import object_kit


@pytest.fixture(scope='module')
def container():
    return object_kit.Container()


def test_container_items_blank(container):
    assert not container.__items__


def test_container_append(container):
    container.Append('foo')
    container.Append('bar')
    assert container.__items__ == ['foo', 'bar']


def test_container_count(container):
    assert container.Count('foo') == 1
    assert container.Count('bar') == 1


def test_container_index(container):
    assert container.Index('foo') == 0
    assert container.Index('bar') == 1


def test_container_extend(container):
    container.Extend(['baz', 'qux'])
    assert container.__items__ == ['foo', 'bar', 'baz', 'qux']


def test_container_insert(container):
    container.Insert(0, 'baz')
    assert container.__items__[0] == 'baz'

    container.Insert(1, 'qux')
    assert container.__items__[1] == 'qux'


def test_container_pop(container):
    assert container.Pop(0) == 'baz'
    assert container.Pop(0) == 'qux'


def test_container_remove(container):
    container.Remove('baz')
    assert 'baz' not in container.__items__

    container.Remove('qux')
    assert 'qux' not in container.__items__


def test_container_reverse(container):
    current = [x for x in container.__items__]
    container.Reverse()
    assert container.__items__ == current[::-1]


def test_container_clear(container):
    container.Clear()
    assert not container.__items__


def test_container_sort(container):
    class Item(object):
        def __init__(self, name, value):
            self.name = name
            self.value = value

    container.Append(Item(name='foo', value=1))
    container.Append(Item(name='bar', value=2))
    container.Append(Item(name='baz', value=3))

    container.Sort(attr='name')
    assert container.__items__[0].name == 'bar'
    assert container.__items__[1].name == 'baz'
    assert container.__items__[2].name == 'foo'

    container.Sort(attr='name', descending=True)
    assert container.__items__[0].name == 'foo'
    assert container.__items__[1].name == 'baz'
    assert container.__items__[2].name == 'bar'

    container.Sort(attr='value')
    assert container.__items__[0].value == 1
    assert container.__items__[1].value == 2
    assert container.__items__[2].value == 3

    container.Sort(attr='value', descending=True)
    assert container.__items__[0].value == 3
    assert container.__items__[1].value == 2
    assert container.__items__[2].value == 1


@pytest.fixture(scope='module')
def xml_object():
    return object_kit.XMLObject()


def test_xml_object_set_tag_name(xml_object):
    xml_object.SetTagName(tagName='foo')
    assert xml_object.tagName == 'foo'


def test_xml_object_to_element(xml_object):
    xml_object.ToElement()


def test_xml_object_content(xml_object):
    xml_object.Content()


@pytest.fixture(scope='module')
def xml_container():
    return object_kit.XMLContainer()


def test_xml_container_to_element(xml_container):
    xml_container.ToElement()


@pytest.fixture(scope='module')
def message_container():
    header = {'foo': 'bar'}
    message = 'baz'
    title1 = 'qux'
    title2 = 'quux'
    return object_kit.MessageContainer(header=header, message=message, title1=title1, title2=title2)


def test_message_container(message_container):
    assert message_container.tagName == 'MediaContainer'
    assert message_container.header == {'foo': 'bar'}
    assert message_container.message == 'baz'
    assert message_container.title1 == 'qux'
    assert message_container.title2 == 'quux'


@pytest.fixture(scope='module')
def metadata_item():
    return object_kit.MetadataItem()


def test_metadata_item_init(metadata_item):
    assert metadata_item.xml_tag == 'MetadataItem'


@pytest.fixture(scope='module')
def metadata_search_result():
    id = 1
    name = 'foo'
    year = 1970
    score = 69
    lang = 'en'
    thumb = 'bar.jpg'
    return object_kit.MetadataSearchResult(id=id, name=name, year=year, score=score, lang=lang, thumb=thumb)


def test_metadata_search_result(metadata_search_result):
    assert metadata_search_result.tagName == 'SearchResult'
    assert metadata_search_result.id == 1
    assert metadata_search_result.name == 'foo'
    assert metadata_search_result.year == 1970
    assert metadata_search_result.score == 69
    assert metadata_search_result.lang == 'en'
    assert metadata_search_result.thumb == 'bar.jpg'


@pytest.fixture(scope='module')
def search_result():
    return object_kit.SearchResult()


def test_search_result_init(search_result):
    assert search_result.xml_tag == 'SearchResult'


@pytest.fixture(scope='module')
def part_object():
    return object_kit.PartObject()


def test_part_object(part_object):
    assert part_object.xml_tag == 'Part'


@pytest.fixture(scope='module')
def media_object():
    return object_kit.MediaObject()


def test_media_object(media_object):
    assert media_object.xml_tag == 'Media'


def test_media_object_to_xml(media_object):
    media_object.to_xml()


@pytest.fixture(scope='module')
def webkit_url():
    return object_kit.WebkitURL()


def test_web_video_url():
    url = 'foo.bar'
    returned_url = object_kit.WebVideoURL(url=url)
    assert 'url={}'.format(url) in returned_url


def test_rtmp_video_url():
    url = 'foo.bar'
    returned_url = object_kit.RTMPVideoURL(url=url)
    assert url in returned_url


def test_windows_media_video_url():
    url = 'foo.bar'
    width = 1920
    height = 1080
    returned_url = object_kit.WindowsMediaVideoURL(url=url)
    assert quote('stream={}'.format(url)) in returned_url

    returned_url = object_kit.WindowsMediaVideoURL(url=url, width=width)
    assert quote('width={}'.format(width)) in returned_url

    returned_url = object_kit.WindowsMediaVideoURL(url=url, height=height)
    assert quote('height={}'.format(height)) in returned_url

    returned_url = object_kit.WindowsMediaVideoURL(url=url, width=width, height=height)
    assert quote('height={}'.format(height)) in returned_url
    assert quote('width={}'.format(width)) in returned_url
    assert quote('stream={}'.format(url)) in returned_url


def test_http_live_stream_url():
    url = 'foo.bar'
    returned_url = object_kit.RTMPVideoURL(url=url)
    assert url in returned_url


def test_embed_url():
    url = 'foo.bar'
    returned_url = object_kit.RTMPVideoURL(url=url)
    assert url in returned_url


def test_indirect_response(container):
    object_kit.IndirectResponse(container=container, key='foo')


def test_callback():
    object_kit.Callback(callback_string='foo', url='bar')

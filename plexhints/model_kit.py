# future imports
from __future__ import absolute_import  # import like python 3

# local imports
from plexhints.template_kit import _TemplateKit

# setup Template object
_Template = _TemplateKit()


def _media_proxy_container():
    return _Template.ProxyContainer(_Template.Proxy.Media, _Template.Proxy.Preview)


class Person(_Template.Record):
    role = _Template.String()
    name = _Template.String()
    photo = _Template.String()

    # Interface settings
    xml_attr_name = 'tag'


class Review(_Template.Record):
    author = _Template.String()
    source = _Template.String()
    image = _Template.String()
    link = _Template.String()
    text = _Template.String()


class Chapter(_Template.Record):
    title = _Template.String()
    start_time_offset = _Template.Integer()
    end_time_offset = _Template.Integer()


class Concert(_Template.Record):
    title = _Template.String()
    venue = _Template.String()
    city = _Template.String()
    country = _Template.String()
    date = _Template.String()
    url = _Template.String()


class MetadataModel(object):
    require_key_and_rating_key = True
    id = _Template.String()  # this is the id as populated from the matching process

    guid_args = ['lang']
    genres = _Template.Set(_Template.String())
    tags = _Template.Set(_Template.String())
    collections = _Template.Set(_Template.String())
    reviews = _Template.Set(Review())
    duration = _Template.Integer()
    rating = _Template.Float()
    audience_rating = _Template.Float()
    rating_image = _Template.String()
    audience_rating_image = _Template.String()
    original_title = _Template.String()
    title_sort = _Template.String()
    rating_count = _Template.Integer()

    # Interface settings
    key = _Template.String()
    rating_key = _Template.String()
    source_title = _Template.String()
    genres.xml_tag = 'Genre'
    tags.xml_tag = 'Tag'


class VideoExtra(MetadataModel):
    xml_tag = 'Video'
    xml_attributes = dict(type='clip')
    suppress_source_icon = True
    require_key_and_rating_key = False

    title = _Template.String()
    year = _Template.Integer()
    originally_available_at = _Template.Date()
    studio = _Template.String()
    tagline = _Template.String()
    summary = _Template.String()
    writers = _Template.Set(Person())
    directors = _Template.Set(Person())
    producers = _Template.Set(Person())
    roles = _Template.Set(Person())
    countries = _Template.Set(_Template.String())
    index = _Template.Integer()

    # Interface settings
    writers.xml_tag = 'Writer'
    directors.xml_tag = 'Director'
    producers.xml_tag = 'Producer'
    roles.xml_tag = 'Role'
    countries.xml_tag = 'Country'

    thumb = _Template.String()

    art_url = _Template.String()
    art_url.synthetic_name = 'art'


class Trailer(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='trailer')


class DeletedScene(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='deletedScene')


class BehindTheScenes(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='behindTheScenes')


class Interview(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='interview')


class SceneOrSample(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='sceneOrSample')


class Featurette(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='featurette')


class Short(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='short')


class Other(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='other')


class MusicVideo(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='musicVideo')

    album = _Template.String()
    album.xml_attr_name = 'parentTitle'


class LiveMusicVideo(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='liveMusicVideo')

    album = _Template.String()
    album.xml_attr_name = 'parentTitle'


class LyricMusicVideo(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='lyricMusicVideo')

    album = _Template.String()
    album.xml_attr_name = 'parentTitle'


class ConcertVideo(VideoExtra):
    xml_attributes = dict(type='clip',
                          relation_type='concert')

    album = _Template.String()
    album.xml_attr_name = 'parentTitle'


class Movie(MetadataModel):
    xml_tag = 'Video'
    xml_attributes = dict(type='movie')

    title = _Template.String()
    year = _Template.Integer()
    originally_available_at = _Template.Date()
    studio = _Template.String()
    tagline = _Template.String()
    summary = _Template.String()
    trivia = _Template.String()
    quotes = _Template.String()
    content_rating = _Template.String()
    content_rating_age = _Template.Integer()
    writers = _Template.Set(Person())
    directors = _Template.Set(Person())
    producers = _Template.Set(Person())
    roles = _Template.Set(Person())
    countries = _Template.Set(_Template.String())
    posters = _media_proxy_container()
    art = _media_proxy_container()
    banners = _media_proxy_container()
    themes = _media_proxy_container()
    chapters = _Template.Set(Chapter())
    extras = _Template.ObjectContainer(Trailer, DeletedScene, BehindTheScenes, Interview, SceneOrSample, Featurette,
                                       Short, Other)
    similar = _Template.Set(_Template.String())

    # Interface settings
    writers.xml_tag = 'Writer'
    directors.xml_tag = 'Director'
    producers.xml_tag = 'Producer'
    roles.xml_tag = 'Role'
    countries.xml_tag = 'Country'

    thumb = _Template.String()

    art_url = _Template.String()
    art_url.synthetic_name = 'art'


class VideoClip(Movie):
    xml_attributes = dict(type='clip')


class VideoClipObject(VideoClip):
    def __init__(self, **kwargs):
        pass

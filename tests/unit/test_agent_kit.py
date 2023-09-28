# -*- coding: utf-8 -*-

# lib imports
import pytest

# local imports
from plexhints.agent_kit import _AgentKit, _Media, MediaObject


@pytest.fixture(scope='function')
def media_object():
    media_object = MediaObject()
    return media_object


def test_base_media_class(media_object):
    assert hasattr(media_object, 'primary_agent')
    assert hasattr(media_object, 'primary_metadata')
    assert hasattr(media_object, 'guid')
    assert hasattr(media_object, 'filename')
    assert hasattr(media_object, 'parent_metadata')
    # assert hasattr(media_object, 'parentGUID')
    assert hasattr(media_object, 'tree')
    assert hasattr(media_object, 'id')
    assert hasattr(media_object, 'hash')
    assert hasattr(media_object, 'originally_available_at')


@pytest.fixture(scope='function')
def media():
    media = _Media()
    return media


@pytest.fixture(scope='function')
def movie(media):
    item = media.Movie()
    return item


def test_movie(movie):
    test_base_media_class(movie)
    assert movie._model_name == 'Movie'
    assert movie._type_id == 1

    assert hasattr(movie, 'title')
    assert hasattr(movie, 'primary_metadata')
    assert hasattr(movie, 'name')
    assert hasattr(movie, 'openSubtitlesHash')
    assert hasattr(movie, 'year')
    assert hasattr(movie, 'duration')


@pytest.fixture(scope='function')
def tv_show(media):
    item = media.TV_Show()
    return item


def test_tv_show(tv_show):
    test_base_media_class(tv_show)
    assert tv_show._model_name == 'TV_Show'
    assert tv_show._type_id == 2

    assert hasattr(tv_show, 'show')
    assert hasattr(tv_show, 'season')
    assert hasattr(tv_show, 'episode')
    assert hasattr(tv_show, 'name')
    assert hasattr(tv_show, 'openSubtitlesHash')
    assert hasattr(tv_show, 'year')
    assert hasattr(tv_show, 'duration')
    assert hasattr(tv_show, 'episodic')


@pytest.fixture(scope='function')
def album(media):
    item = media.Album()
    return item


def test_album(album):
    test_base_media_class(album)
    assert album._model_name == 'LegacyAlbum'
    assert album._media_type_name == 'Album'
    assert album._parent_model_name == 'Artist'
    assert album._parent_link_name == 'artist'
    assert album._parent_set_attr_name == 'albums'
    assert album._type_id == 9

    assert hasattr(album, 'name')
    assert hasattr(album, 'artist')
    assert hasattr(album, 'album')
    assert hasattr(album, 'track')
    assert hasattr(album, 'index')
    assert hasattr(album, 'parentGUID')


@pytest.fixture(scope='function')
def artist(media):
    item = media.Artist()
    return item


def test_artist(artist):
    test_base_media_class(artist)
    assert artist._model_name == 'LegacyArtist'
    assert artist._media_type_name == 'Artist'
    assert artist._type_id == 8

    assert hasattr(artist, 'artist')
    assert hasattr(artist, 'album')
    assert hasattr(artist, 'track')
    assert hasattr(artist, 'index')


@pytest.fixture(scope='function')
def photo_album(media):
    item = media.PhotoAlbum()
    return item


def test_photo_album(photo_album):
    test_base_media_class(photo_album)
    assert photo_album._model_name == 'PhotoAlbum'
    assert photo_album._type_id == 12


@pytest.fixture(scope='function')
def photo(media):
    item = media.Photo()
    return item


def test_photo(photo):
    test_base_media_class(photo)
    assert photo._model_name == 'Photo'
    assert photo._type_id == 13


@pytest.fixture(scope='function')
def agent_kit():
    agent_kit = _AgentKit()
    return agent_kit


@pytest.fixture(scope='function')
def album_agent(agent_kit):
    agent = agent_kit.Album()
    return agent


def test_album_agent(album_agent, media):
    assert hasattr(album_agent, 'name')
    assert hasattr(album_agent, 'media_type')

    assert album_agent.name == 'Album'
    assert album_agent.media_type == media.Album


@pytest.fixture(scope='function')
def artist_agent(agent_kit):
    agent = agent_kit.Artist()
    return agent


def test_artist_agent(artist_agent, media):
    assert hasattr(artist_agent, 'name')
    assert hasattr(artist_agent, 'media_type')

    assert artist_agent.name == 'Artist'
    assert artist_agent.media_type == media.Artist


@pytest.fixture(scope='function')
def movies_agent(agent_kit):
    agent = agent_kit.Movies()
    return agent


def test_movies_agent(movies_agent, media):
    assert hasattr(movies_agent, 'name')
    assert hasattr(movies_agent, 'media_type')

    assert movies_agent.name == 'Movies'
    assert movies_agent.media_type == media.Movie


@pytest.fixture(scope='function')
def photos_agent(agent_kit):
    agent = agent_kit.Photos()
    return agent


def test_photos_agent(photos_agent, media):
    assert hasattr(photos_agent, 'name')
    assert hasattr(photos_agent, 'media_type')

    assert photos_agent.name == 'Photos'
    assert photos_agent.media_type == media.Photo


@pytest.fixture(scope='function')
def tv_shows_agent(agent_kit):
    agent = agent_kit.TV_Shows()
    return agent


def test_tv_shows_agent(tv_shows_agent, media):
    assert hasattr(tv_shows_agent, 'name')
    assert hasattr(tv_shows_agent, 'media_type')

    assert tv_shows_agent.name == 'TV_Shows'
    assert tv_shows_agent.media_type == media.TV_Show

# -*- coding: utf-8 -*-

# local imports
from plexhints import model_kit
from plexhints import template_kit


def test_media_proxy_container():
    container = model_kit._media_proxy_container()
    assert isinstance(container, template_kit._TemplateKit.ProxyContainer)


def test_person():
    person = model_kit.Person()
    assert isinstance(person, template_kit._TemplateKit.Record)
    assert isinstance(person.role, template_kit._TemplateKit.String)
    assert isinstance(person.name, template_kit._TemplateKit.String)
    assert isinstance(person.photo, template_kit._TemplateKit.String)
    assert person.xml_attr_name == 'tag'


def test_review():
    review = model_kit.Review()
    assert isinstance(review, template_kit._TemplateKit.Record)
    assert isinstance(review.author, template_kit._TemplateKit.String)
    assert isinstance(review.source, template_kit._TemplateKit.String)
    assert isinstance(review.image, template_kit._TemplateKit.String)
    assert isinstance(review.link, template_kit._TemplateKit.String)
    assert isinstance(review.text, template_kit._TemplateKit.String)


def test_chapter():
    chapter = model_kit.Chapter()
    assert isinstance(chapter, template_kit._TemplateKit.Record)
    assert isinstance(chapter.title, template_kit._TemplateKit.String)
    assert isinstance(chapter.start_time_offset, template_kit._TemplateKit.Integer)
    assert isinstance(chapter.end_time_offset, template_kit._TemplateKit.Integer)


def test_concert():
    concert = model_kit.Concert()
    assert isinstance(concert, template_kit._TemplateKit.Record)
    assert isinstance(concert.title, template_kit._TemplateKit.String)
    assert isinstance(concert.venue, template_kit._TemplateKit.String)
    assert isinstance(concert.city, template_kit._TemplateKit.String)
    assert isinstance(concert.country, template_kit._TemplateKit.String)
    assert isinstance(concert.date, template_kit._TemplateKit.String)
    assert isinstance(concert.url, template_kit._TemplateKit.String)


def test_metadata_model():
    metadata_model = model_kit.MetadataModel()
    assert metadata_model.require_key_and_rating_key
    assert isinstance(metadata_model.id, template_kit._TemplateKit.String)
    assert metadata_model.guid_args == ['lang']
    assert isinstance(metadata_model.genres, template_kit._TemplateKit.Set)
    assert isinstance(metadata_model.tags, template_kit._TemplateKit.Set)
    assert isinstance(metadata_model.collections, template_kit._TemplateKit.Set)
    assert isinstance(metadata_model.reviews, template_kit._TemplateKit.Set)
    assert isinstance(metadata_model.duration, template_kit._TemplateKit.Integer)
    assert isinstance(metadata_model.rating, template_kit._TemplateKit.Float)
    assert isinstance(metadata_model.audience_rating, template_kit._TemplateKit.Float)
    assert isinstance(metadata_model.rating_image, template_kit._TemplateKit.String)
    assert isinstance(metadata_model.audience_rating_image, template_kit._TemplateKit.String)
    assert isinstance(metadata_model.original_title, template_kit._TemplateKit.String)
    assert isinstance(metadata_model.title_sort, template_kit._TemplateKit.String)
    assert isinstance(metadata_model.rating_count, template_kit._TemplateKit.Integer)

    assert isinstance(metadata_model.key, template_kit._TemplateKit.String)
    assert isinstance(metadata_model.rating_key, template_kit._TemplateKit.String)
    assert isinstance(metadata_model.source_title, template_kit._TemplateKit.String)
    assert metadata_model.genres.xml_tag == 'Genre'
    assert metadata_model.tags.xml_tag == 'Tag'


def test_video_extra():
    video_extra = model_kit.VideoExtra()
    assert video_extra.xml_attributes['type'] == 'clip'

    assert isinstance(video_extra, model_kit.MetadataModel)
    assert isinstance(video_extra.title, template_kit._TemplateKit.String)
    assert isinstance(video_extra.year, template_kit._TemplateKit.Integer)
    assert isinstance(video_extra.originally_available_at, template_kit._TemplateKit.Date)
    assert isinstance(video_extra.studio, template_kit._TemplateKit.String)
    assert isinstance(video_extra.tagline, template_kit._TemplateKit.String)
    assert isinstance(video_extra.summary, template_kit._TemplateKit.String)
    assert isinstance(video_extra.writers, template_kit._TemplateKit.Set)
    assert isinstance(video_extra.directors, template_kit._TemplateKit.Set)
    assert isinstance(video_extra.producers, template_kit._TemplateKit.Set)
    assert isinstance(video_extra.roles, template_kit._TemplateKit.Set)
    assert isinstance(video_extra.countries, template_kit._TemplateKit.Set)
    assert isinstance(video_extra.index, template_kit._TemplateKit.Integer)
    assert isinstance(video_extra.thumb, template_kit._TemplateKit.String)
    assert isinstance(video_extra.art_url, template_kit._TemplateKit.String)

    assert video_extra.xml_tag == 'Video'
    assert video_extra.writers.xml_tag == 'Writer'
    assert video_extra.directors.xml_tag == 'Director'
    assert video_extra.producers.xml_tag == 'Producer'
    assert video_extra.roles.xml_tag == 'Role'
    assert video_extra.countries.xml_tag == 'Country'
    assert video_extra.art_url.synthetic_name == 'art'


def test_trailer():
    uut = model_kit.Trailer()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'trailer'


def test_deleted_scene():
    uut = model_kit.DeletedScene()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'deletedScene'


def test_behind_the_scenes():
    uut = model_kit.BehindTheScenes()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'behindTheScenes'


def test_interview():
    uut = model_kit.Interview()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'interview'


def test_scene_or_sample():
    uut = model_kit.SceneOrSample()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'sceneOrSample'


def test_featurette():
    uut = model_kit.Featurette()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'featurette'


def test_short():
    uut = model_kit.Short()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'short'


def test_other():
    uut = model_kit.Other()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'other'


def test_music_video():
    uut = model_kit.MusicVideo()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'musicVideo'
    assert isinstance(uut.album, template_kit._TemplateKit.String)
    assert uut.album.xml_attr_name == 'parentTitle'


def test_live_music_video():
    uut = model_kit.LiveMusicVideo()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'liveMusicVideo'
    assert isinstance(uut.album, template_kit._TemplateKit.String)
    assert uut.album.xml_attr_name == 'parentTitle'


def test_lyric_music_video():
    uut = model_kit.LyricMusicVideo()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'lyricMusicVideo'
    assert isinstance(uut.album, template_kit._TemplateKit.String)
    assert uut.album.xml_attr_name == 'parentTitle'


def test_concert_video():
    uut = model_kit.ConcertVideo()
    assert isinstance(uut, model_kit.VideoExtra)
    assert uut.xml_attributes['type'] == 'clip'
    assert uut.xml_attributes['relation_type'] == 'concert'
    assert isinstance(uut.album, template_kit._TemplateKit.String)
    assert uut.album.xml_attr_name == 'parentTitle'


def test_movie():
    movie = model_kit.Movie()
    assert movie.xml_attributes['type'] == 'movie'

    assert isinstance(movie, model_kit.MetadataModel)
    assert isinstance(movie.title, template_kit._TemplateKit.String)
    assert isinstance(movie.year, template_kit._TemplateKit.Integer)
    assert isinstance(movie.originally_available_at, template_kit._TemplateKit.Date)
    assert isinstance(movie.studio, template_kit._TemplateKit.String)
    assert isinstance(movie.tagline, template_kit._TemplateKit.String)
    assert isinstance(movie.summary, template_kit._TemplateKit.String)
    assert isinstance(movie.trivia, template_kit._TemplateKit.String)
    assert isinstance(movie.quotes, template_kit._TemplateKit.String)
    assert isinstance(movie.content_rating, template_kit._TemplateKit.String)
    assert isinstance(movie.content_rating_age, template_kit._TemplateKit.Integer)
    assert isinstance(movie.writers, template_kit._TemplateKit.Set)
    assert isinstance(movie.directors, template_kit._TemplateKit.Set)
    assert isinstance(movie.producers, template_kit._TemplateKit.Set)
    assert isinstance(movie.roles, template_kit._TemplateKit.Set)
    assert isinstance(movie.countries, template_kit._TemplateKit.Set)
    assert isinstance(movie.posters, template_kit._TemplateKit.ProxyContainer)
    assert isinstance(movie.art, template_kit._TemplateKit.ProxyContainer)
    assert isinstance(movie.banners, template_kit._TemplateKit.ProxyContainer)
    assert isinstance(movie.themes, template_kit._TemplateKit.ProxyContainer)
    assert isinstance(movie.chapters, template_kit._TemplateKit.Set)
    assert isinstance(movie.extras, template_kit._TemplateKit.ObjectContainer)
    assert isinstance(movie.similar, template_kit._TemplateKit.Set)
    assert isinstance(movie.thumb, template_kit._TemplateKit.String)
    assert isinstance(movie.art_url, template_kit._TemplateKit.String)

    assert movie.xml_tag == 'Video'
    assert movie.writers.xml_tag == 'Writer'
    assert movie.directors.xml_tag == 'Director'
    assert movie.producers.xml_tag == 'Producer'
    assert movie.roles.xml_tag == 'Role'
    assert movie.countries.xml_tag == 'Country'
    assert movie.art_url.synthetic_name == 'art'


def test_video_clip():
    uut = model_kit.VideoClip()
    assert isinstance(uut, model_kit.Movie)
    assert uut.xml_attributes['type'] == 'clip'


def test_video_clip_object():
    uut = model_kit.VideoClipObject()
    assert isinstance(uut, model_kit.VideoClip)
    assert uut.xml_attributes['type'] == 'clip'

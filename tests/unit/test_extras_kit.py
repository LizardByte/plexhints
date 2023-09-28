# -*- coding: utf-8 -*-

# local imports
from plexhints import extras_kit


def test_extras_kit():
    title_arg = 'title'
    file_arg = 'file'
    thumb_arg = 'thumb'
    url_arg = 'url'
    uut = extras_kit._ExtrasKit(title=title_arg, file=file_arg, thumb=thumb_arg, url=url_arg)
    assert uut.title == title_arg
    assert uut.file == file_arg
    assert uut.thumb == thumb_arg
    assert uut.url == url_arg


def test_extras_kit_predefined():
    title_arg = 'title'
    file_arg = 'file'
    thumb_arg = 'thumb'
    url_arg = 'url'

    test_units = [
        extras_kit.BehindTheScenesObject,
        extras_kit.ConcertVideoObject,
        extras_kit.DeletedSceneObject,
        extras_kit.FeaturetteObject,
        extras_kit.InterviewObject,
        extras_kit.LiveMusicVideoObject,
        extras_kit.LyricMusicVideoObject,
        extras_kit.MusicVideoObject,
        extras_kit.OtherObject,
        extras_kit.SceneOrSampleObject,
        extras_kit.ShortObject,
        extras_kit.TrailerObject,
    ]

    for test_unit in test_units:
        assert test_unit is extras_kit._ExtrasKit

        test_object = test_unit(title=title_arg, file=file_arg, thumb=thumb_arg, url=url_arg)
        assert test_object.title == title_arg
        assert test_object.file == file_arg
        assert test_object.thumb == thumb_arg
        assert test_object.url == url_arg

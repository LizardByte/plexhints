# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
from typing import Optional

# local imports
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()


class MediaObject(object):
    """
    A MediaObject represents a media item discovered by PMS and encapsulates any information
    provided by the server. It is intended to provide hints to metadata agents when
    finding metadata to download.
    """

    _attrs = dict()
    _model_name = None
    _versioned_model_names = {}
    _media_type_name = None
    _parent_model_name = None
    _parent_link_name = None
    _parent_set_attr_name = None
    _type_id = 0
    _level_names = []
    _level_attribute_keys = []

    def __init__(self, access_point=None, version=None, **kwargs):
        self._access_point = access_point
        self.primary_agent = None  # type: Optional[str]
        self.primary_metadata = None  # type: Optional[str]
        self.guid = None  # type: Optional[str]
        self.filename = None  # type: Optional[str]
        self.parent_metadata = None  # type: Optional[str]
        self.parentGUID = None  # type: Optional[str]
        self.tree = None
        self.id = None  # type: Optional[str]
        self.hash = None  # type: Optional[str]
        self.originally_available_at = None  # type: Optional[int]

        cls = type(self)
        for name in cls._attrs:
            setattr(self, name, cls._attrs[name])

        for name in kwargs:
            if hasattr(self, name):
                setattr(self, name, kwargs[name])

        # Get the media tree if we got an ID passed down.
        if self.id is not None:
            try:
                setattr(self, 'tree', _Media.TreeForDatabaseID(dbid=self.id, level_names=type(self)._level_names,
                                                               level_attribute_keys=type(self)._level_attribute_keys))
            except Exception:
                _Log.Exception(fmt="Exception when constructing media object")

        # Load primary agent's metadata.
        if self.primary_agent is not None and self.guid is not None:
            # todo
            self.primary_metadata = None

        # Load the parent's metadata.
        if self.parentGUID and cls._parent_model_name:
            # todo
            self.parent_metadata = None

        del self.parentGUID

    def __getattr__(self, name):
        if hasattr(self, 'tree') and hasattr(self.tree, name):
            return getattr(self.tree, name)
        else:
            return object.__getattribute__(self, name)


class _Media(object):

    @classmethod
    def TreeForDatabaseID(cls, dbid, level_names=[], host='127.0.0.1', parent_id=None, level_attribute_keys=[]):
        # type: (str, list, str, Optional[str], list) -> Optional[dict]
        # todo
        tree = None
        return tree

    class Movie(MediaObject):
        def __init__(self, **kwargs):
            super(_Media.Movie, self).__init__(**kwargs)
            self._model_name = 'Movie'
            self._type_id = 1
            self._attrs = dict()  # removed in favor of defining values below

            self.primary_metadata = None  # type: Optional[str]
            self.name = None  # type: Optional[str]
            self.openSubtitlesHash = None  # type: Optional[str]
            self.year = None  # type: Optional[int]
            self.duration = None  # type: Optional[int]

            # todo - couldn't find in Plex framework, but this property does exist
            self.title = None  # type: Optional[str]

    class TV_Show(MediaObject):
        def __init__(self, **kwargs):
            super(_Media.TV_Show, self).__init__(**kwargs)
            self._model_name = 'TV_Show'
            self._type_id = 2
            self._attrs = dict()  # removed in favor of defining values below
            self._level_names = ['seasons', 'episodes']

            self.show = None  # type: Optional[str]
            self.season = None  # type: Optional[int]
            self.episode = None  # type: Optional[int]
            self.name = None  # type: Optional[str]
            self.openSubtitlesHash = None  # type: Optional[str]
            self.year = None  # type: Optional[int]
            self.duration = None  # type: Optional[int]
            self.episodic = True  # type: bool

    class Album(MediaObject):
        def __init__(self, **kwargs):
            super(_Media.Album, self).__init__(**kwargs)
            self._model_name = 'LegacyAlbum'
            self._media_type_name = 'Album'
            self._parent_model_name = 'Artist'
            self._parent_link_name = 'artist'
            self._parent_set_attr_name = 'albums'
            self._type_id = 9
            self._attrs = dict()  # removed in favor of defining values below
            self._level_names = ['tracks']

            self.name = None  # type: Optional[str]
            self.artist = None  # type: Optional[str]
            self.album = None  # type: Optional[str]
            self.track = None  # type: Optional[str]
            self.index = None  # type: Optional[int]
            self.parentGUID = None  # type: Optional[str]

    class Artist(MediaObject):
        def __init__(self, **kwargs):
            super(_Media.Artist, self).__init__(**kwargs)
            self._model_name = 'LegacyArtist'
            self._versioned_model_names = {
                2: 'ModernArtist'
            }
            self._media_type_name = 'Artist'
            self._type_id = 8
            self._attrs = dict()  # removed in favor of defining values below
            self._level_names = ['albums', 'tracks']
            self._level_attribute_keys = ['guid']

            self.artist = None  # type: Optional[str]
            self.album = None  # type: Optional[str]
            self.track = None  # type: Optional[str]
            self.index = None  # type: Optional[int]

    class PhotoAlbum(MediaObject):
        def __init__(self, **kwargs):
            super(_Media.PhotoAlbum, self).__init__(**kwargs)
            self._model_name = 'PhotoAlbum'
            self._type_id = 12
            self._attrs = dict()
            self._level_names = ['photos']

    class Photo(MediaObject):
        def __init__(self, **kwargs):
            super(_Media.Photo, self).__init__(**kwargs)
            self._model_name = 'Photo'
            self._type_id = 13
            self._attrs = dict()


class _AgentKit:
    """
    Fake Agent class with available subclasses.

    https://web.archive.org/web/https://dev.plexapp.com/docs/agents/basics.html#defining-an-agent-class
    """

    def __init__(self):
        pass

    class Album:
        """
        This is a fake Agent.Album class.
        """

        def __init__(self):
            self.name = 'Album'
            self.media_type = Media.Album

    class Artist:
        """
        This is a fake Agent.Artist class.
        """

        def __init__(self):
            self.name = 'Artist'
            self.media_type = Media.Artist

    class Movies:
        """
        This is a fake Agent.Movies class.
        """

        def __init__(self):
            self.name = 'Movies'
            self.media_type = Media.Movie

    class Photos:
        """
        This is a fake Agent.Photos class.

        .. Note:: This class is undocumented in the original docs, but appears to be available in the Framework.
        """

        def __init__(self):
            self.name = 'Photos'
            self.media_type = Media.Photo

    class TV_Shows:
        """This is a fake Agent.TV_Shows class."""

        def __init__(self):
            self.name = 'TV_Shows'
            self.media_type = Media.TV_Show


Agent = _AgentKit()
Media = _Media()

# future imports
from __future__ import absolute_import  # import like python 3

# local imports
from plexhints.log_kit import LogKit

# setup logging
Log = LogKit()


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

    def __init__(self, access_point, version=None, **kwargs):
        self._access_point = access_point
        self.primary_agent = None
        self.primary_metadata = None
        self.guid = None
        self.filename = None
        self.parent_metadata = None
        self.parentGUID = None
        self.tree = None
        self.id = None
        self.hash = None
        self.originally_available_at = None

        cls = type(self)
        for name in cls._attrs:
            setattr(self, name, cls._attrs[name])

        for name in kwargs:
            if hasattr(self, name):
                setattr(self, name, kwargs[name])

        # Get the media tree if we got an ID passed down.
        if self.id is not None:
            try:
                setattr(self, 'tree', Media.TreeForDatabaseID(self.id, type(self)._level_names,
                                                              level_attribute_keys=type(self)._level_attribute_keys))
            except Exception:
                Log.Exception(fmt="Exception when constructing media object")

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


class Media(object):

    @classmethod
    def TreeForDatabaseID(cls, dbid, level_names=[], host='127.0.0.1', parent_id=None, level_attribute_keys=[]):
        # todo
        tree = None
        return tree

    class Movie(MediaObject):
        _model_name = 'Movie'
        _type_id = 1
        _attrs = dict(
            primary_metadata=None,
            name=None,
            openSubtitlesHash=None,
            year=None,
            duration=None,
        )

    class TV_Show(MediaObject):
        _model_name = 'TV_Show'
        _type_id = 2
        _attrs = dict(
            show=None,
            season=None,
            episode=None,
            name=None,
            openSubtitlesHash=None,
            year=None,
            duration=None,
            episodic=True
        )
        _level_names = ['seasons', 'episodes']

    class Album(MediaObject):
        _model_name = 'LegacyAlbum'
        _media_type_name = 'Album'
        _parent_model_name = 'Artist'
        _parent_link_name = 'artist'
        _parent_set_attr_name = 'albums'
        _type_id = 9
        _attrs = dict(
            name=None,
            artist=None,
            album=None,
            track=None,
            index=None,
            parentGUID=None
        )
        _level_names = ['tracks']

    class Artist(MediaObject):
        _model_name = 'LegacyArtist'
        _versioned_model_names = {
            2: 'ModernArtist'
        }
        _media_type_name = 'Artist'
        _type_id = 8
        _attrs = dict(
            artist=None,
            album=None,
            track=None,
            index=None
        )
        _level_names = ['albums', 'tracks']
        _level_attribute_keys = ['guid']

    class PhotoAlbum(MediaObject):
        _model_name = 'PhotoAlbum'
        _type_id = 12
        _attrs = dict()
        _level_names = ['photos']

    class Photo(MediaObject):
        _model_name = 'Photo'
        _type_id = 13
        _attrs = dict()


class AgentKit:
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

        This class is undocumented in the original docs, but appears to be available in the Framework.
        """

        def __init__(self):
            self.name = 'Photos'
            self.media_type = Media.Photo

    class TV_Shows:
        """This is a fake Agent.TV_Shows class."""

        def __init__(self):
            self.name = 'TV_Shows'
            self.media_type = Media.TV_Show

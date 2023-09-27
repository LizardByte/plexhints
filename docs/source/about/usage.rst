:github_url: https://github.com/LizardByte/plexhints/tree/nightly/docs/source/about/usage.rst

Usage
=====
Plexhints can be used by just importing the ``plexhints`` module and running a couple of functions. After doing so
you can use plexhints in your IDE and run most of your code outside of Plex. This is useful for debugging and testing.

Main Entry Point
----------------
Place this at the top of your ``Contents/Code/__init__.py`` file. It is important to only import these when running
outside of Plex.

.. code-block:: python

   # plex debugging
   try:
       import plexhints  # noqa: F401
   except ImportError:
       pass
   else:  # the code is running outside of Plex
       from plexhints import plexhints_setup, update_sys_path
       plexhints_setup()  # reads the plugin plist file and determine if plexhints should use elevated policy or not
       update_sys_path()  # when running outside plex, append the path

Submodules
----------
In files other than the main ``__init__.py`` file, you can simply import the ``plexhints`` module and use it as shown.

.. code-block:: python

   # plex debugging
   try:
       import plexhints  # noqa: F401
   except ImportError:
       pass
   else:  # the code is running outside of Plex
       from plexhints.log_kit import Log

Available Imports
-----------------

.. code-block:: python

   from plexhints.agent_kit import Agent, Media  # agent kit
   from plexhints.core_kit import Core  # core kit
   from plexhints.decorator_kit import handler, indirect, route  # decorator kit
   from plexhints.exception_kit import Ex  # exception kit
   from plexhints.locale_kit import Locale  # locale kit
   from plexhints.log_kit import Log  # log kit
   from plexhints.model_kit import Movie, VideoClip, VideoClipObject  # model kit
   from plexhints.network_kit import HTTP  # network kit
   from plexhints.object_kit import Callback, IndirectResponse, MediaObject, MessageContainer, MetadataItem, \
       MetadataSearchResult, PartObject, SearchResult  # object kit
   from plexhints.parse_kit import HTML, JSON, Plist, RSS, XML, YAML  # parse kit
   from plexhints.prefs_kit import Prefs  # prefs kit
   from plexhints.proxy_kit import Proxy  # proxy kit
   from plexhints.resource_kit import Resource  # resource kit
   from plexhints.shortcut_kit import L, E, D, R, S  # shortcut kit
   from plexhints.util_kit import String, Util  # util kit

   from plexhints.constant_kit import CACHE_1MINUTE, CACHE_1HOUR, CACHE_1DAY, CACHE_1WEEK, CACHE_1MONTH  # constant kit
   from plexhints.constant_kit import ClientPlatforms, Protocols, OldProtocols, ServerPlatforms, ViewTypes, \
       SummaryTextTypes, AudioCodecs, VideoCodecs, Containers, ContainerContents, \
       StreamTypes  # constant kit, more commonly used in URL services

   # extra objects
   from plexhints.extras_kit import BehindTheScenesObject, \
       ConcertVideoObject, \
       DeletedSceneObject, \
       FeaturetteObject, \
       InterviewObject, \
       LiveMusicVideoObject, \
       LyricMusicVideoObject, \
       MusicVideoObject, \
       OtherObject, \
       SceneOrSampleObject, \
       ShortObject, \
       TrailerObject

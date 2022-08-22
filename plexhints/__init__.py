# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import os

# local imports
from plexhints import _constants
# import kits
from plexhints.agent_kit import AgentKit, Media
from plexhints import constant_kit
from plexhints.core_kit import CoreKit
from plexhints.extras_kit import ExtrasKit
from plexhints.locale_kit import LocaleKit
from plexhints.log_kit import LogKit
from plexhints.network_kit import HTTPKit
from plexhints.parse_kit import HTMLKit, JSONKit, PlistKit, RSSKit, XMLKit, YAMLKit
from plexhints.prefs_kit import PreferenceSet
from plexhints.proxy_kit import ProxyKit
from plexhints.object_kit import MessageContainer, MetadataItem, MetadataSearchResult, SearchResult  # noqa: F401
from plexhints.util_kit import UtilKit

# agent kit
Agent = AgentKit()
Media = Media()

# core kit
Core = CoreKit()

# network kit
HTTP = HTTPKit()

# locale kit
Locale = LocaleKit()

# log kit
Log = LogKit()

# parse kit
HTML = HTMLKit()
JSON = JSONKit()
Plist = PlistKit()
RSS = RSSKit()
XML = XMLKit()
YAML = YAMLKit()

# prefs kit
Prefs = PreferenceSet('test')

# proxy kit
Proxy = ProxyKit()

# util kit
Util = UtilKit()

# extras kit
BehindTheScenesObject = ExtrasKit()
ConcertVideoObject = ExtrasKit()
DeletedSceneObject = ExtrasKit()
FeaturetteObject = ExtrasKit()
InterviewObject = ExtrasKit()
LiveMusicVideoObject = ExtrasKit()
LyricMusicVideoObject = ExtrasKit()
MusicVideoObject = ExtrasKit()
OtherObject = ExtrasKit()
SceneOrSampleObject = ExtrasKit()
ShortObject = ExtrasKit()
TrailerObject = ExtrasKit()

# constants used by plug-ins
CACHE_1MINUTE = constant_kit.CACHE_1MINUTE
CACHE_1HOUR = constant_kit.CACHE_1HOUR
CACHE_1DAY = constant_kit.CACHE_1DAY
CACHE_1WEEK = constant_kit.CACHE_1WEEK
CACHE_1MONTH = constant_kit.CACHE_1MONTH

# open the plugin's Plist file and see if it has an elevated policy
plist_file = os.path.join('Contents', 'Info.plist')
with open(plist_file, mode='r') as f:
    plist_dict = PlistKit().ObjectFromString(string=f.read())

    try:
        if plist_dict['PlexPluginCodePolicy'] == 'Elevated':
            _constants.ELEVATED_POLICY = True
    except KeyError:
        pass

    del plist_dict

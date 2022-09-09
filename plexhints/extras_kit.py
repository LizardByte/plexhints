# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
from typing import Any, Optional

# local imports
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()


class _ExtrasKit:
    def __init__(self, title=None, file=None, thumb=None, url=None, **kwargs):
        # type: (Optional[str], Optional[str], Optional[str], Optional[str], **Any) -> None
        self.title = title
        self.file = file
        self.thumb = thumb
        self.url = url

        if kwargs:
            _Log.Debug('The following kwargs are not handled by plexhints, '
                       'although they should be processed by the plex framework: %s' % kwargs)


BehindTheScenesObject = _ExtrasKit
ConcertVideoObject = _ExtrasKit
DeletedSceneObject = _ExtrasKit
FeaturetteObject = _ExtrasKit
InterviewObject = _ExtrasKit
LiveMusicVideoObject = _ExtrasKit
LyricMusicVideoObject = _ExtrasKit
MusicVideoObject = _ExtrasKit
OtherObject = _ExtrasKit
SceneOrSampleObject = _ExtrasKit
ShortObject = _ExtrasKit
TrailerObject = _ExtrasKit

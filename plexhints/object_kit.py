# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
from future.moves.urllib.parse import quote, quote_plus
import operator
from typing import Optional

# redefine unicode
try:
    unicode
except NameError:
    unicode = str


class Container(object):

    def __init__(self, **kwargs):
        self.__items__ = []

    def Append(self, obj):
        # type: (any) -> None
        if obj is not None:
            return self.__items__.append(obj)

    def Count(self, x):
        # type: (any) -> int
        return self.__items__.count(x)

    def Index(self, x):
        # type: (any) -> int
        return self.__items__.index(x)

    def Extend(self, x):
        # type: (any) -> None
        return self.__items__.extend(x)

    def Insert(self, i, x):
        # type: (int, any) -> None
        if i is not None:
            return self.__items__.insert(i, x)

    def Pop(self, i):
        # type: (int) -> any
        return self.__items__.pop(i)

    def Remove(self, x):
        # type: (any) -> None
        """
        Remove first occurrence of value. Raises ValueError if the value is not present.

        Parameters
        ----------
        x : any
            The value to remove.
        """
        return self.__items__.remove(x)

    def Reverse(self):
        # type: () -> None
        self.__items__.reverse()

    def Sort(self, attr, descending=False):
        # type: (any, bool) -> None
        self.__items__.sort(key=operator.attrgetter(attr))
        if descending:
            self.__items__.reverse()

    def Clear(self):
        # type: () -> None
        self.__items__ = []


class XMLObject(object):
    def __init__(self, **kwargs):
        self.tagName = self.__class__.__name__

    def SetTagName(self, tagName):
        self.tagName = tagName

    def ToElement(self):
        pass

    def Content(self):
        pass


class XMLContainer(XMLObject, Container):
    def __init__(self, **kwargs):
        super(XMLContainer, self).__init__(**kwargs)
        self.tagName = self.__class__.__name__

    def ToElement(self):
        pass


class MessageContainer(XMLContainer):
    def __init__(self, header, message, title1=None, title2=None, **kwargs):
        XMLContainer.__init__(self, header=header, message=message, title1=title1, title2=title2, noCache=True,
                              **kwargs)
        self.tagName = "MediaContainer"  # type: str
        self.header = header  # type: dict
        self.message = message  # type: str
        self.title1 = title1  # type: str
        self.title2 = title2  # type: str


class MetadataItem(Container):
    xml_tag = 'MetadataItem'

    def __init__(self):
        super(MetadataItem, self).__init__()
        self.type = None  # type: Optional[any]  # todo - what type is actually used
        self.id = None  # type: Optional[str]
        self.title = None  # type: Optional[str]
        self.guid = None  # type: Optional[str]
        self.index = None  # type: Optional[int]
        self.originally_available_at = None  # type: Optional[int]
        self.score = None  # type: Optional[int]
        self.thumb = None  # type: Optional[str]
        self.matched = None  # type: Optional[bool]


class MetadataSearchResult(XMLObject):
    def __init__(self, id, name=None, year=None, score=0, lang=None, thumb=None):
        XMLObject.__init__(self, id=id, thumb=thumb, name=name, year=year, score=score, lang=lang)
        self.tagName = "SearchResult"  # type: str
        self.id = id  # type: Optional[str]
        self.name = name  # type: Optional[str]
        self.year = year  # type: Optional[int]
        self.score = score  # type: Optional[int]
        self.lang = lang  # type: Optional[str]
        self.thumb = thumb  # type: Optional[str]


class SearchResult(Container):
    xml_tag = 'SearchResult'

    def __init__(self):
        super(SearchResult, self).__init__()
        self.type = None  # type: Optional[any]  # todo - what type is actually used
        self.id = None  # type: Optional[str]
        self.name = None  # type: Optional[str]
        self.guid = None  # type: Optional[str]
        self.index = None  # type: Optional[int]
        self.year = None  # type: Optional[int]
        self.score = None  # type: Optional[int]
        self.thumb = None  # type: Optional[str]
        self.matched = None  # type: Optional[bool]
        self.parentName = None  # type: Optional[str]
        self.parentID = None  # type: Optional[str]
        self.parentGUID = None  # type: Optional[str]
        self.parentIndex = None  # type: Optional[int]


class PartObject(Container):
    xml_tag = 'Part'

    def __int__(self, **kwargs):
        self.key = None
        self.file = None
        self.duration = None
        self.http_headers = None
        self.container = None
        self.optimized_for_streaming = None
        self.duration = None
        self.protocol = None

        if 'file' not in kwargs:
            self.file = ''


class MediaObject(Container):
    xml_tag = 'Media'

    def __init__(self, **kwargs):
        super(MediaObject, self).__init__(**kwargs)
        self.protocols = None
        self.platforms = None
        self.bitrate = None
        self.aspect_ratio = None
        self.audio_channels = None
        self.audio_codec = None
        self.video_codec = None
        self.video_resolution = None
        self.container = None
        self.video_frame_rate = None
        self.duration = None
        self.width = None
        self.height = None
        self.protocol = None
        self.optimized_for_streaming = None

    def to_xml(self):
        pass


class WebkitURL(unicode):
    pass


def WebVideoURL(url):
    # type: (str) -> WebkitURL
    prefix = None
    return WebkitURL("plex://127.0.0.1/video/:/webkit?url=%s&prefix=%s" % (quote_plus(url), prefix))


def RTMPVideoURL(url, clip=None, clips=None, width=None, height=None, live=False, swf_url=None, app=None, args=None,
                 **kwargs):
    # type: (str, Optional[any], Optional[any], Optional[int], Optional[int], bool, Optional[any], Optional[any], Optional[any], **any) -> str  # noqa: E501  # is it possible to have multiline type hints in python2?
    # todo
    return url


def WindowsMediaVideoURL(url, width=None, height=None):
    # type: (str, Optional[int], Optional[int]) -> WebkitURL
    final_url = "https://www.plexapp.com/player/silverlight.php?stream={}".format(quote(url))
    if width:
        final_url = "{}&width={}".format(final_url, width)
    if height:
        final_url = "{}&height={}".format(final_url, height)

    return WebVideoURL(final_url)


def HTTPLiveStreamURL(url):
    # type: (str) -> str
    # todo
    return url


def EmbedURL(url):
    # type: (str) -> str
    # todo
    return url


def IndirectResponse(container, key, **kwargs):
    # type: (Container, str, **any) -> None
    pass


def Callback(callback_string, url, **kwargs):
    # type: (any, str, **any) -> None
    pass

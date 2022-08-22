# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import operator


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
        self.tagName = "MediaContainer"
        self.header = header
        self.message = message
        self.title1 = title1
        self.title2 = title2


class MetadataItem(Container):
    xml_tag = 'MetadataItem'

    def __init__(self):
        super(MetadataItem, self).__init__()
        self.type = None
        self.id = None
        self.title = None
        self.guid = None
        self.index = None
        self.originally_available_at = None
        self.score = None
        self.thumb = None
        self.matched = None


class MetadataSearchResult(XMLObject):
    def __init__(self, id, name=None, year=None, score=0, lang=None, thumb=None):
        XMLObject.__init__(self, id=id, thumb=thumb, name=name, year=year, score=score, lang=lang)
        self.tagName = "SearchResult"


class SearchResult(Container):
    xml_tag = 'SearchResult'

    def __init__(self):
        super(SearchResult, self).__init__()
        self.type = None
        self.id = None
        self.name = None
        self.guid = None
        self.index = None
        self.year = None
        self.score = None
        self.thumb = None
        self.matched = None
        self.parentName = None
        self.parentID = None
        self.parentGUID = None
        self.parentIndex = None

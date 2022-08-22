# future imports
from __future__ import absolute_import  # import like python 3


class ProxyObject(object):
    def __init__(self, proxy_name, proxy_type, data=None, sort_order=None, ext=None, index=None, codec=None,
                 format=None, default=None, forced=None, **kwargs):
        self._proxy_name = proxy_name
        self._proxy_type = proxy_type
        self._data = data
        self._sort_order = sort_order
        self._ext = ext
        self._index = index
        self._codec = codec
        self._format = format
        self._default = default
        self._forced = forced
        self._extras = kwargs

    def __getitem__(self, name):
        return self._extras.get(name)

    def __setitem__(self, name, value):
        self._extras[name] = value


class ProxyKit(object):
    def __init__(self):
        self.Preview = ProxyObject(proxy_name='Preview', proxy_type='preview')
        self.Media = ProxyObject(proxy_name='Media', proxy_type='media')
        self.LocalFile = ProxyObject(proxy_name='LocalFile', proxy_type='localfile')
        self.Remote = ProxyObject(proxy_name='Remote', proxy_type='remote')

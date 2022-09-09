# future imports
from __future__ import absolute_import  # import like python 3

# local imports
from plexhints.template_kit import _ProxyObject


def proxy_object_generator(proxy_name):
    # type: (str) -> object
    def proxy_function(data, sort_order=None, ext=None, index=None, **kwargs):
        # type: (bytes, int, str, int, **any) -> _ProxyObject
        return _ProxyObject(proxy_name=proxy_name, proxy_type=proxy_name.lower(), data=data, sort_order=sort_order,
                            ext=ext, index=index, **kwargs)

    return proxy_function


class _ProxyKit(object):
    def __init__(self):
        self.Preview = proxy_object_generator(proxy_name='Preview')
        self.Media = proxy_object_generator(proxy_name='Media')
        self.LocalFile = proxy_object_generator(proxy_name='LocalFile')
        self.Remote = proxy_object_generator(proxy_name='Remote')


Proxy = _ProxyKit()

# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import datetime
import os
import shutil
import weakref

# local imports
from plexhints.core_kit import _CoreKit

_Core = _CoreKit()


# redefine unicode
try:
    unicode
except NameError:
    unicode = str


# attributes
class _Combinable(object):
    pass


class _Serializable(object):
    def _serialize(self, path):
        raise Exception("_serialize not implemented in subclass %s" % type(self).__name__)

    def _deserialize(self, path, el):
        raise Exception("_deserialize not implemented in subclass %s" % type(self).__name__)

    def _writedata(self, path, data):
        os.makedirs(os.path.dirname(path))
        el = _Core.data.xml.element(self._name)
        el.set('external', str(True))
        if self._data_ext is not None:
            el.set('extension', str(self._data_ext))
            path += '.' + self._data_ext
        _Core.storage.save(path, data)
        return el

    def _readdata(self, path):
        if self._data_ext is not None:
            path += '.' + self._data_ext
        if os.path.exists(path):
            return _Core.storage.load(path)

    def _deletedata(self, path):
        if self._data_ext is not None:
            path += '.' + self._data_ext
        if os.path.exists(path):
            os.unlink(path)


class _AttributeSet(object):
    def __getattribute__(self, name):
        if name[0] != '_' and name in self._attributes:
            return self._attributes[name]._getcontent()
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name[0] == '_':
            object.__setattr__(self, name, value)

        # Only allow setting the id if the model isn't read-only
        elif name == 'id':
            if self._access_point._read_only:
                raise Exception("Data for %s instance %s provided by %s can't be modified" % (
                    type(self).__name__, self._uid, self.provider))
            self._id = value

        elif name in self._attributes:
            try:
                self._attributes[name]._setcontent(value)
            except Exception:
                # print "Exception setting attribute '%s' of %s to %s" % (name, str(self), str(value))
                raise

        else:
            raise AttributeError("'%s' object has no attribute named '%s'" % (type(self).__name__, name))

    # Separate getter/setter for synthetic attributes - these can only be set via interfaces
    def _has_synthetic_attr(self, name):
        return name in self._synthetic_attributes

    def _get_synthetic_attr(self, name):
        if name in self._synthetic_attributes:
            return self._synthetic_attributes[name]._getcontent()
        raise Exception("No synthetic attribute named '%s' found" % name)

    def _set_synthetic_attr(self, name, value):
        if name in self._synthetic_attributes:
            try:
                self._synthetic_attributes[name]._setcontent(value)
                return
            except Exception:
                # print "Exception setting synthetic attribute '%s' of %s to %s" % (name, str(self), str(value))
                raise
        raise Exception("No synthetic attribute named '%s' found" % name)


class _AttributeObject(object):

    def __init__(self, owner, template, name):
        self._owner_ref = weakref.ref(owner)
        self._template_ref = weakref.ref(template)
        self._name = name
        if hasattr(self, '_init'):
            self._init()

    @property
    def _owner(self):
        return self._owner_ref()

    @property
    def _template(self):
        return self._template_ref()

    @property
    def _core(self):
        return self._owner._core

    @property
    def _external(self):
        return self._template._external

    @property
    def _data_ext(self):
        return self._template._data_ext

    @property
    def _access_point(self):
        return self._owner._access_point

    @property
    def _model(self):
        return self._owner._model

    def _getcontent(self):
        pass

    def _setcontent(self, content):
        if self._access_point._read_only:
            raise Exception("Data for %s instance %s provided by %s can't be modified" % (
                type(self._model).__name__, self._model._uid, self._access_point._identifier))

    def _save(self):
        self._owner._save()


class _ValueObject(_AttributeObject, _Serializable):
    _type = None

    def _init(self):
        self._value = None

    def _getcontent(self):
        return self._value

    def _setcontent(self, content):
        _AttributeObject._setcontent(self, content)
        if content is not None and not isinstance(content, type(self)._type):
            raise AttributeError("Provided content of type '%s' is not of the required type '%s'." % (
                type(content).__name__, type(self)._type.__name__))
        self._value = content
        self._save()

    def _serialize(self, path):
        el = self.__Core.data.xml.element(self._name)
        content = self._getcontent()

        if content is not None or self._template._allows_null:
            try:
                el.text = unicode(content)
            except NameError:
                el.text = content
            except Exception:
                print("Exception serializing '%s'" % unicode(content))
                raise

        if self._external:
            el = self._writedata(path, str(content))

        return el

    def _deserialize(self, path, el):
        if bool(el.get("external")):
            content_str = self._readdata(path)
        else:
            content_str = el.text
        try:
            if content_str is None or content_str == 'None':
                self._value = None
            else:
                self._value = type(self)._type(content_str)
        except Exception:
            print("Error deserializing " + content_str)
            raise

    def _to_string(self):
        content = self._getcontent()
        if content or self._template._allows_null:
            return unicode(content)

    def setcontent(self, content):
        self._setcontent(content)


class _StringObject(_ValueObject):
    _type = unicode

    def _setcontent(self, content):
        _AttributeObject._setcontent(self, content)
        if not (content is None or isinstance(content, unicode)):
            content = unicode(content)
        _ValueObject._setcontent(self, content)


class _IntegerObject(_ValueObject):
    _type = int


class _FloatObject(_ValueObject):
    _type = float


class _BooleanObject(_ValueObject):
    _type = bool


class _DateObject(_ValueObject):
    _type = datetime.date

    def _setcontent(self, content):
        if isinstance(content, datetime.datetime):
            content = content.date()
        return _ValueObject._setcontent(self, content)

    def _deserialize(self, path, el):
        if bool(el.get("external")):
            content_str = self._readdata(path)
        else:
            content_str = el.text
        if content_str is not None and len(content_str) > 0:
            self._value = datetime.datetime.strptime(content_str, "%Y-%m-%d").date()


class _TimeObject(_ValueObject):
    _type = datetime.time
    # TODO: deserialization


class _DatetimeObject(_ValueObject):
    _type = datetime.datetime
    # TODO: deserialization


class _DataObject(_AttributeObject, _Serializable):

    def _init(self):
        self._data = str()

    def _getcontent(self):
        return self._data

    def _setcontent(self, content):
        _AttributeObject._setcontent(self, content)
        self._data = str(content)
        self._save()

    def _serialize(self, path):
        if not self._external:
            raise Exception("Data objects must always be saved externally.")
        else:
            content_str = str(self._getcontent())
            return self._writedata(path, content_str)

    def _deserialize(self, path, el=None):
        content_str = self._readdata(path)
        self._data = content_str


class _ContainerObject(_AttributeObject, _Serializable):
    def _getcontent(self):
        return self

    def _setcontent(self, content):
        raise Exception("Container-type attributes can't be assigned directly.")


class _ObjectContainerObject(_ContainerObject):
    def _init(self):
        self._container = self.__Core.sandbox.environment['ObjectContainer']()

    def _getcontent(self):
        return self._container

    def _serialize(self, path):
        if not self._external:
            raise Exception("Container objects must always be saved externally.")

        if len(self._container) > 0:
            # Validate objects within the container to ensure they inherit from the correct template class.
            for obj in self._container.objects:
                if not hasattr(obj, '_template') or obj._template not in self._template._classes:
                    names = [cls.__name__ for cls in self._template._classes]
                    raise Exception("Unable to serialize object of type '%s', should be in %s" % (
                        obj._template.__name__, str(names)))

            xml = self._container._to_xml()
            content_str = self.__Core.data.xml.to_string(xml)
            return self._writedata(path, content_str)
        else:
            self._deletedata(path)

    def _deserialize(self, path, el=None):
        # We don't currently support deserializing container XML; add if/when it's required.
        pass


class _ItemObject(_AttributeObject):
    def __init__(self, obj, name):
        _AttributeObject.__init__(self, obj._owner, obj._template, name)
        self._obj = obj

    def _getcontent(self): return self._obj._getcontent()

    def _setcontent(self, content): return self._obj._setcontent(content)

    @property
    def _external(self): return self._obj._external

    @property
    def _data_ext(self): return self._obj._data_ext


class _MapItem(_ItemObject, _Serializable):
    _attr_name = 'key'

    def _serialize(self, path):
        if not isinstance(self._obj, _Serializable):
            raise Exception("Mapping item %s is not serializable!" % repr(self._obj))
        attr_el = self._obj._serialize(path)

        if attr_el is not None:
            attr_el.set(type(self)._attr_name, self._name)

            # If the item has its own index, use that as the key & set our name as the "guid" attribute.
            index_els = attr_el.xpath('index')
            if len(index_els):
                index_el = index_els[0]
                if index_el.text is not None:
                    attr_el.set('guid', self._name)
                    attr_el.set(type(self)._attr_name, index_el.text)
                    attr_el.remove(index_el)

        return attr_el


class _MapObject(_ContainerObject, _Serializable):
    _item_class = _MapItem

    def _init(self):
        self._items = dict()

    def _serialize(self, path):
        el = self.__Core.data.xml.element(self._name)

        if os.path.exists(path):
            shutil.rmtree(path)

        for name in self._items:
            item = self._items[name]
            item_name = self.__Core.data.hashing.sha1(
                item._name) if self._model._template.use_hashed_map_paths else item._name
            item_el = item._serialize(os.path.join(path, item_name))

            if item_el is not None:
                el.append(item_el)

        if self._external:
            el = self._writedata(path, self.__Core.data.xml.to_string(el))

        return el

    def _deserialize(self, path, el):
        if bool(el.get('external')):
            el = self.__Core.data.xml.from_string(self._readdata(path))
        for item_el in el.getchildren():
            name = item_el.get(type(self)._item_class._attr_name)

            # Check if we have a GUID - if so, reassign it as the name & set the original name as the index property
            # after deserializing the object.
            #
            guid = item_el.get('guid')
            if guid is not None:
                index = name
                name = guid

            obj = self._template._item_template._new(self, 'item')
            obj._deserialize(os.path.join(path, name), item_el)

            self._items[name] = type(self)._item_class(obj, name)

            if guid is not None:
                self._items[name].index = index

    def __getitem__(self, name):
        name = unicode(name)

        if name in self._items:
            return self._items[name]._obj._getcontent()
        elif isinstance(self._template._item_template, _RecordTemplate):
            obj = self._template._item_template._new(self, 'item')
            self._items[name] = type(self)._item_class(obj, name)
            return self._items[name]._getcontent()

    def __setitem__(self, name, value):
        name = unicode(name)

        if name in self._items:
            self._items[name]._obj._setcontent(value)
        else:
            obj = self._template._item_template._new(self, 'item')
            obj._setcontent(value)
            self._items[name] = type(self)._item_class(obj, name)
            self._save()

    def __delitem__(self, name):
        if name in self._items:
            del self._items[name]

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return self._items.__len__()

    def __contains__(self, name):
        return name in self._items

    def keys(self):
        return self._items.keys()

    def validate_keys(self, valid_keys):
        for key in self.keys():
            if key not in valid_keys:
                del self[key]


class _DirectoryObject(_MapObject, _Serializable, _Combinable):

    def _init(self):
        if not isinstance(self._template._item_template, _DataTemplate):
            raise Exception("Incorrect template type (%s): Directory attributes can only hold Data items." %
                            self._template._item_template)
        _MapObject._init(self)

    def _serialize(self, path):
        # Same as above, but don't append item elements to the XML
        el = self.__Core.data.xml.element(self._name)

        if os.path.exists(path):
            shutil.rmtree(path)

        for name in self._items:
            item = self._items[name]
            item._serialize(os.path.join(path, item._name))

        if self._external:
            el = self._writedata(path, self.__Core.data.xml.to_string(el))

        return el

    def _deserialize(self, path, el):
        if os.path.exists(path):
            for name in os.listdir(path):
                obj = self._template._item_template._new(self, 'item')
                obj._deserialize(os.path.join(path, name), el)
                self._items[name] = type(self)._item_class(obj, name)


class _ProxyObject(object):

    def __init__(self, proxy_name, proxy_type, data, sort_order=None, ext=None, index=None, codec=None, format=None,
                 default=None, forced=None, **kwargs):
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


class _ProxiedDataObject(_DataObject):

    def _init(self):
        _DataObject._init(self)
        self._proxy_type = 'unknown'
        self._sort_order = None
        self._format = None

    def _setcontent(self, content):
        self._proxy_type = content._proxy_type
        self._sort_order = content._sort_order
        self._format = content._format
        _DataObject._setcontent(self, content._data)


class _ProxyContainerItem(_MapItem):
    _attr_name = 'url'

    def __init__(self, obj, name):
        if not isinstance(obj, _ProxiedDataObject):
            raise Exception("Incorrect object type (%s): Must be a Proxied Data object." % type(obj))
        _MapItem.__init__(self, obj, name)

    @property
    def _proxy_type(self):
        return self._obj._proxy_type

    @_proxy_type.setter
    def _proxy_type(self, value):
        self._obj._proxy_type = value

    @property
    def _sort_order(self):
        return self._obj._sort_order

    @_sort_order.setter
    def _sort_order(self, value):
        self._obj._sort_order = value

    @property
    def _format(self):
        return self._obj._format

    @_format.setter
    def _format(self, value):
        self._obj._format = value


class _ProxyContainerObject(_MapObject, _Serializable, _Combinable):
    _item_class = _ProxyContainerItem

    def _init(self):
        if not isinstance(self._template._item_template, _DataTemplate):
            raise Exception("Incorrect template type (%s): ProxyContainer attributes can only hold Data items." %
                            self._template._item_template)
        _MapObject._init(self)

    def _serialize(self, path):
        el = self.__Core.data.xml.element(self._name)

        if os.path.exists(path):
            shutil.rmtree(path)

        sorted_items = {}
        other_items = []

        for url in self._items:
            item = self._items[url]
            url_hash = self.__Core.data.hashing.sha1(url)
            item_el = item._serialize(os.path.join(path, url_hash))

            if item_el is not None:
                item_el.set(item._proxy_type, url_hash)

                if item._format:
                    item_el.set('format', str(item._format))

                if item._sort_order:
                    item_el.set('sort_order', str(item._sort_order))
                    if item._sort_order not in sorted_items:
                        sorted_items[item._sort_order] = []
                    sorted_items[item._sort_order].append(item_el)
                else:
                    other_items.append(item_el)

        for order in sorted(sorted_items.keys()):
            for item_el in sorted_items[order]:
                el.append(item_el)

        for item_el in other_items:
            el.append(item_el)

        return el

    def _deserialize(self, path, el):
        for item_el in el.getchildren():
            attr_name = type(self)._item_class._attr_name
            url = item_el.get(attr_name)
            proxy_type = 'unknown'

            for key in item_el.keys():
                if key not in [attr_name, 'external']:
                    proxy_type = key
                    break

            url_hash = self.__Core.data.hashing.sha1(url)
            obj = self._template._item_template._new(self, 'item')
            obj._proxy_type = proxy_type
            if 'sort_order' in item_el.attrib:
                obj._sort_order = int(item_el.attrib['sort_order'])
            obj._deserialize(os.path.join(path, url_hash), item_el)
            self._items[url] = type(self)._item_class(obj, url)

    def __setitem__(self, name, value):
        if not isinstance(value, _ProxyObject):
            raise Exception("Incorrect value type (%s): Must be a Proxy object." % type(value))
        if value._proxy_name not in self._template._accepted_proxies:
            raise Exception("Proxy type '%s' is not accepted by this attribute." % value._proxy_name)
        _MapObject.__setitem__(self, name, value)

    def hasSortOrder(self, name):
        name = unicode(name)

        if name in self._items:
            return self._items[name]._obj._sort_order is not None
        return False

    def sort_these_keys_first(self, key_set):
        index = 1
        index_end = 10000
        for key in self._items:
            if key in key_set:
                self._items[key]._obj._sort_order = index
                index = index + 1
            else:
                self._items[key]._obj._sort_order = index_end
                index_end = index_end + 1


class _SetItem(_ItemObject, _Serializable):
    def _serialize(self, path):
        if not isinstance(self._obj, _Serializable):
            raise Exception("Set item %s is not serializable!" % repr(self._obj))
        attr_el = self._obj._serialize(path)
        return attr_el


class _SetObject(_ContainerObject, _Serializable, _Combinable):
    def __init__(self, owner, template, name):
        super(_SetObject, self).__init__(owner, template, name)
        self._items = None

    def _init(self):
        self._items = list()

    def add(self, value):
        obj = self._template._item_template._new(self, 'item')
        obj._setcontent(value)
        self._items.append(obj)
        self._save()

    def clear(self):
        self._items = list()
        self._save()

    def new(self):
        if not isinstance(self._template._item_template, _RecordTemplate):
            raise Exception("This attribute type does not support creating new instances.")
        obj = self._template._item_template._new(self, 'item')
        self._items.append(obj)
        self._save()
        return obj

    def find(self, **kwargs):
        for item in self._items:
            found = True
            content = item._getcontent()
            for name in kwargs:
                value = kwargs[name]
                if not (hasattr(content, name) and getattr(content, name) == value):
                    found = False
            if found:
                return content

    def _serialize(self, path):
        el = self.__Core.data.xml.element(self._name)

        count = 0
        for item in self._items:
            attr_el = item._serialize(os.path.join(path, str(count)))
            if attr_el is not None:
                attr_el.set('index', str(count))
                el.append(attr_el)
            count += 1

        if self._external:
            el = self._writedata(path, self.__Core.data.xml.to_string(el))

        return el

    def _deserialize(self, path, el):
        if bool(el.get("external")):
            el = self.__Core.data.xml.from_string(self._readdata(path))

        for item_el in el.getchildren():
            obj = self._template._item_template._new(self, 'item')
            obj._deserialize(os.path.join(path, item_el.get("index")), item_el)
            self._items.append(obj)

    # TODO: Exceptions
    def __getitem__(self, pos):
        if 0 <= pos < len(self._items):
            return self._items[pos]._getcontent()

    def __setitem__(self, pos, value):
        if 0 <= pos < len(self._items):
            self._items[pos]._setcontent(value)
            self._save()

    def __iter__(self):
        lst = list()
        for item in self._items:
            lst.append(item._getcontent())
        return lst.__iter__()

    def __len__(self):
        return self._items.__len__()

    def _setcontent(self, content):
        if isinstance(content, list):
            self.clear()
            for item in content:
                self.add(item)
        else:
            _ContainerObject._setcontent(self, content)


class _LinkObject(_AttributeObject, _Serializable):

    def _init(self):
        self._link_uid = None

    def _serialize(self, path):
        if self._external:
            raise Exception("Link attributes can't be saved externally.")
        el = self.__Core.data.xml.element(self._name)
        if self._link_uid:
            el.text = self._link_uid
        return el

    def _deserialize(self, path, el):
        self._link_uid = el.text

    def _getcontent(self):
        if self._link_uid:
            cls = getattr(self._access_point, self._template._item_template.__name__)
            return cls[self._link_uid]

    def _setcontent(self, content):
        _AttributeObject._setcontent(self, content)
        cls = getattr(self._access_point, self._template._item_template.__name__)
        if str(type(content)) != str(cls):
            raise Exception("Attribute must be set to a %s object" % cls.__name__)
        else:
            self._link_uid = content._uid
            content._write()
            self._save()


class _RecordObject(_AttributeObject, _AttributeSet, _Serializable, _Combinable):

    def _init(self):
        attrs = dict()
        cls = type(self._template)
        for name in dir(cls):
            template = getattr(cls, name)

            if isinstance(template, _AttributeTemplate):
                attrs[name] = template._new(self, name)

        self.__dict__['_attributes'] = attrs

    def _getcontent(self):
        return self

    def _serialize(self, path):
        el = self.__Core.data.xml.element(self._name)

        for name in self._attributes:
            attr = self._attributes[name]
            attr_el = attr._serialize(os.path.join(path, attr._name))
            if attr_el is not None:
                el.append(attr_el)

        if self._external:
            el.tag = type(self._template).__name__
            el = self._writedata(path, self.__Core.data.xml.to_string(el))

        return el

    def _deserialize(self, path, el):
        if bool(el.get('external')):
            el = self.__Core.data.xml.from_string(self._readdata(path))
        if el is not None:
            for attr_el in el.getchildren():
                if attr_el.tag in self._attributes:
                    attr = self._attributes[attr_el.tag]
                    attr._deserialize(os.path.join(path, attr_el.tag), attr_el)


# templates
class _AbstractTemplate(object):
    pass


class _XMLGeneratingObjectTemplate(object):
    xml_tag = 'Object'
    xml_attributes = {}
    http_response_status = 200
    http_response_headers = {}


class _ModelTemplate(_XMLGeneratingObjectTemplate):
    guid_args = []
    use_hashed_map_paths = False


class _AttributeTemplate(object):
    _object_type = None
    _data_ext = None
    _always_external = False
    xml_attr_name = None

    # Specifies whether this type should always be excluded from model interfaces
    _always_exclude_from_interface = False

    def __init__(self):
        self._external = type(self)._always_external
        self._exclude_from_interface = type(self)._always_exclude_from_interface

        # Specifies whether the attribute should only be available via model interfaces
        self._synthetic = False

        # Specifies whether the attribute should be serialised even if it has a null value
        self._allows_null = False

        # Specifies whether the synthetic attribute should be renamed
        # (workaround for synthetic & regular attributes with the same name, e.g. 'art')
        self.synthetic_name = None

    def _new(self, owner, name):
        return type(self)._object_type(owner, self, name)

    @property
    def save_externally(self):
        self._external = True

    @property
    def exclude_from_interface(self):
        self._exclude_from_interface = True

    @property
    def is_synthetic(self):
        self._synthetic = True

    @property
    def allows_null(self):
        self._allows_null = True


class _ReferenceTemplate(_AttributeTemplate):
    def __init__(self, item_template):
        _AttributeTemplate.__init__(self)
        self._item_template = item_template


class _ContainerTemplate(_ReferenceTemplate):
    xml_tag = 'Container'
    xml_attr_name = 'tag'

    @property
    def save_items_externally(self):
        self._item_template.save_externally

    @property
    def exclude_from_interface(self):
        self._item_template.exclude_from_interface


class _ValueTemplate(_AttributeTemplate):
    pass


class _StringTemplate(_ValueTemplate):
    _object_type = _StringObject
    _data_ext = 'txt'


class _IntegerTemplate(_ValueTemplate):
    _object_type = _IntegerObject
    _data_ext = 'int'


class _BooleanTemplate(_ValueTemplate):
    _object_type = _BooleanObject
    _data_ext = 'bool'


class _FloatTemplate(_ValueTemplate):
    _object_type = _FloatObject
    _data_ext = 'float'


class _DateTemplate(_ValueTemplate):
    _object_type = _DateObject
    _data_ext = 'date'


class _TimeTemplate(_ValueTemplate):
    _object_type = _TimeObject
    _data_ext = 'time'


class _DatetimeTemplate(_ValueTemplate):
    _object_type = _DatetimeObject
    _data_ext = 'datetime'


class _DataTemplate(_AttributeTemplate):
    _object_type = _DataObject
    _data_ext = None
    _always_external = True


class _ObjectContainerTemplate(_AttributeTemplate, set):
    def __init__(self, *classes):
        super(_ObjectContainerTemplate, self).__init__()
        self._classes = classes

    _object_type = _ObjectContainerObject
    _data_ext = "xml"
    _always_external = True


class _RecordTemplate(_AttributeTemplate, _XMLGeneratingObjectTemplate):
    _object_type = _RecordObject
    _data_ext = 'xml'


class _MapTemplate(_ContainerTemplate):
    _object_type = _MapObject
    _data_ext = 'xml'


class _DirectoryTemplate(_MapTemplate):
    _object_type = _DirectoryObject
    _data_ext = 'xml'
    _always_exclude_from_interface = True

    def __init__(self):
        _MapTemplate.__init__(self, _DataTemplate())


class _ProxyTemplate(object):
    def __init__(self, name):
        self._name = name


class _ProxiedDataTemplate(_DataTemplate):
    _object_type = _ProxiedDataObject


class _ProxyContainerTemplate(_DirectoryTemplate, dict):
    _object_type = _ProxyContainerObject

    def __init__(self, *proxies):
        self._accepted_proxies = []
        for proxy in proxies:
            if not isinstance(proxy, _ProxyTemplate):
                raise Exception("Proxy containers must only contain proxy objects, not %s" % repr(proxy))
            self._accepted_proxies.append(proxy._name)
        _MapTemplate.__init__(self, _ProxiedDataTemplate())


class _SetTemplate(_ContainerTemplate, set):
    _object_type = _SetObject
    _data_ext = 'xml'


class _LinkTemplate(_ReferenceTemplate):
    _object_type = _LinkObject
    _data_ext = 'xml'

    def __init__(self, item_template):
        # Only allow links to model classes
        if not hasattr(item_template, '__mro__') or (
                hasattr(item_template, '__mro__') and _ModelTemplate not in item_template.__mro__):
            raise Exception("Links must connect to a model class, not %s" % str(item_template))
        _ReferenceTemplate.__init__(self, item_template)


# template kits
class _ProxyTemplateKit(object):
    Preview = _ProxyTemplate(name='Preview')
    Media = _ProxyTemplate(name='Media')
    LocalFile = _ProxyTemplate(name='LocalFile')
    Remote = _ProxyTemplate(name='Remote')


class _TemplateKit(object):
    """
    TemplateKit is a very simple API that provides access to template classes for use when defining model templates.
    """

    Abstract = _AbstractTemplate
    Model = _ModelTemplate
    Record = _RecordTemplate
    Link = _LinkTemplate

    Set = _SetTemplate
    Map = _MapTemplate
    Directory = _DirectoryTemplate
    ProxyContainer = _ProxyContainerTemplate

    String = _StringTemplate
    Integer = _IntegerTemplate
    Float = _FloatTemplate
    Boolean = _BooleanTemplate
    Date = _DateTemplate
    Time = _TimeTemplate
    Datetime = _DatetimeTemplate

    Data = _DataTemplate
    Proxy = _ProxyTemplateKit

    ObjectContainer = _ObjectContainerTemplate

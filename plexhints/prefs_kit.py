# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import json
import os
from typing import Optional, Union

# local imports
from plexhints import CONTENTS
from plexhints.log_kit import _LogKit
from plexhints.parse_kit import _XMLKit

# setup logging
_Log = _LogKit()

# setup xml
_XML = _XMLKit()


class _Pref(object):
    """
    Base class for a Preference object.

    Attributes
    ----------
    type : str
        The type of the preference. Will be one of ``'text'``, ``'bool'``, ``'enum'``.
    label : str
        The label of the preference. This is what Plex displays in the interface for the combined title/description.
    default_value : str
        The default value encoded to a string.
    secure : bool
        True if the value should not be transmitted over http.
    hidden : bool
        Unknown.

    Methods
    -------
    encode_value:
        The encode a value to string.
    decode_value:
        Decode a string value.
    info_dict:
        Return a dictionary with the attributes of the class, plus the current value.
    """

    def __init__(self, pref_type, label, default_value=None, secure=False, hidden=False):
        # type: (str, str, str, bool, bool) -> None
        self.type = pref_type
        self.label = label
        self.default_value = self.encode_value(default_value)
        self.secure = secure
        self.hidden = hidden

    def encode_value(self, value):
        # type: (Union[bool, str, int]) -> str
        """Convert value to ``str``."""
        return value

    def decode_value(self, encoded_value):
        # type: (str) -> Union[bool, str]
        """Convert str to standard python format."""
        return encoded_value

    def info_dict(self, locale, value=None, **kwargs):
        data = dict(
            label=self.label,  # localization.localize(self.label, locale),  # todo - localize the label
            type=self.type,
            secure='true' if self.secure else 'false',
            value=self.default_value if value is None else self.encode_value(value),
            default=self.default_value,
        )

        data.update(**kwargs)
        return data

    def __str__(self):
        return "%s (%s)" % (type(self).__name__, self.label)


class _TextPref(_Pref):
    """
    Base class for a Text Preference object.

    Attributes
    ----------
    type : str
        The type of the preference. Will be ``'text'``.
    label : str
        The label of the preference. This is what Plex displays in the interface for the combined title/description.
    default_value : str
        The default value encoded to a string.
    secure : bool
        True if the value should not be transmitted over http.
    hidden : bool
        Unknown.
    options : list
        A list of preference options. Only known option is `hidden`.

    Methods
    -------
    encode_value:
        Encode a value to string.
    decode_value:
        Decode a string value.
    info_dict:
        Return a dictionary with the attributes of the class, plus the current value.
    """

    def __init__(self, label, default_value, options=[], secure=False, hidden=False):
        _Pref.__init__(self, pref_type='text', label=label, default_value=default_value, secure=secure, hidden=hidden)
        self.type = 'text'
        self.options = options

    def encode_value(self, encoded_value):
        # type: (any) -> str
        if encoded_value is None:
            return ''
        else:
            return str(encoded_value)

    def decode_value(self, value):
        if value is None or len(value) == 0:
            return None
        else:
            return str(value)

    def info_dict(self, locale, value=None, **kwargs):
        data = _Pref.info_dict(self, locale, value, option=','.join(self.options), **kwargs)
        return data


class _BooleanPref(_Pref):
    """
    Base class for a Preference object.

    Attributes
    ----------
    type : str
        The type of the preference. Will be ``'bool'``.
    label : str
        The label of the preference. This is what Plex displays in the interface for the combined title/description.
    default_value : str
        The default value encoded to a string.
    secure : bool
        True if the value should not be transmitted over http.
    hidden : bool
        Unknown.

    Methods
    -------
    encode_value:
        The encode a value to string.
    decode_value:
        Decode a string value.
    info_dict:
        Return a dictionary with the attributes of the class, plus the current value.
    """

    def __init__(self, label, default_value, secure=False, hidden=False):
        _Pref.__init__(self, pref_type='bool', label=label, default_value=default_value, secure=secure, hidden=hidden)
        self.type = 'bool'

    def encode_value(self, value):
        # type: (Union[bool, str]) -> str
        if value is True or str(value).lower() == 'true':
            return 'true'
        else:
            return 'false'

    def decode_value(self, encoded_value):
        # type: (Union[bool, str]) -> bool
        if encoded_value is True or str(encoded_value).lower() == 'true':
            return True
        else:
            return False


class _EnumPref(_Pref):
    """
    Base class for a Preference object.

    Attributes
    ----------
    type : str
        The type of the preference. Will be ``'enum'``.
    label : str
        The label of the preference. This is what Plex displays in the interface for the combined title/description.
    default_value : str
        The default value encoded to a string.
    secure : bool
        True if the value should not be transmitted over http.
    hidden : bool
        Unknown.
    values : list
        A list of possible values represented as strings.

    Methods
    -------
    encode_value:
        The encode a value to string.
    decode_value:
        Decode a string value.
    info_dict:
        Return a dictionary with the attributes of the class, plus the current value.
    """

    def __init__(self, label, default_value, values=[], secure=False, hidden=False):
        self.type = 'enum'
        self.values = values
        _Pref.__init__(self, pref_type='enum', label=label, default_value=default_value, secure=secure, hidden=hidden)

    def encode_value(self, value):
        # type: (str) -> Optional[str]
        """
        Encode enum value.

        Parameters
        ----------
        value : str
            The value to encode.

        Returns
        -------
        Optional[str]
            An integer formatted as a string, representing the index of the value.
        """
        if value in self.values:
            return str(self.values.index(value))
        else:
            return None

    def decode_value(self, encoded_value):
        # type: (Union[int, str]) -> Optional[str]
        try:
            int_val = int(encoded_value)
        except TypeError:
            pass
        else:
            if int_val < len(self.values):
                return self.values[int_val]

    def info_dict(self, locale, value=None, **kwargs):
        value_labels = []
        for v in self.values:
            value_labels.append(v)
            # value_labels.append(localization.localize(v, locale))  # todo - localize value
        return _Pref.info_dict(self, locale, value, values='|'.join(value_labels))


class _PreferenceSet(object):

    def __init__(self, identifier):
        self._identifier = identifier
        self._pref_names = []
        self._prefs_dict = None
        self._prefs_lock = True
        self._user_values_dict = {}
        self._user_values_lock = False

    @property
    def _user_file_path(self):
        return os.path.join('plexhints', 'Preferences', '{}.xml'.format(self._identifier))

    def _load_user_file(self):
        # todo
        # Return immediately if daemonized

        # Check whether the prefs file exists. If not, write defaults and get out.
        file_path = self._user_file_path
        user_values = {}

        if not os.path.isfile(file_path):
            _Log.Info("No user preferences file exists")
            self._save_user_file()

        else:
            # Load the prefs file
            try:
                with open(file_path, mode='r') as f:
                    prefs_xml_str = f.read()

                prefs_xml = _XML.ElementFromString(string=prefs_xml_str)

                # Iterate through each element
                for element in prefs_xml:
                    pref_name = str(element.tag)

                    # If a pref exists with this name, set its value
                    if element.text is not None and pref_name in self._prefs:
                        user_values[pref_name] = str(element.text)

                _Log.Debug("%s the user preferences for %s",
                           ("Loaded" if len(self._user_values_dict) == 0 else "Reloaded"), self._identifier)

            except Exception:
                _Log.Exception("Exception loading user preferences from %s", file_path)

        self._user_values_dict = user_values

    def _save_user_file(self):
        # return immediately if daemonized
        # todo

        element = _XML.Element(name='PluginPreferences')

        for name, pref in self._prefs.items():
            element.append(_XML.Element(name=name,
                                        text=self._user_values_dict.get(name, pref.encode_value(pref.default_value))))

        prefs_xml = _XML.StringFromElement(el=element)
        prefs_directory = os.path.join('plexhints', 'Preferences')
        if not os.path.isdir(prefs_directory):
            os.mkdir(prefs_directory)
        with open(self._user_file_path, mode='w+') as f:
            f.write(prefs_xml)
        _Log.Debug("Saved the user preferences")

    @property
    def _user_values(self):
        # If the user prefs file doesn't exist, or if its mtime has changed, reload it.
        # todo - implement mtime
        if not os.path.isfile(self._user_file_path):
            self._load_user_file()

        return self._user_values_dict

    def update_user_values(self, **kwargs):
        for name, value in kwargs.items():
            if isinstance(self._prefs.get(name), _BooleanPref):
                value = 'true' if str(value).lower() in ['1', 'true'] else 'false'
            self._user_values_dict[name] = value

        self._save_user_file()

    @property
    def _prefs(self):
        if self._prefs_dict is None:
            self._load_prefs()
        return self._prefs_dict

    @property
    def default_prefs_path(self):
        return os.path.join(*CONTENTS + ['DefaultPrefs.json'])

    def _load_prefs(self):
        prefs_dict = {}
        file_paths = []
        prefs_json = []

        # Load the plug-in's DefaultPrefs.json.
        file_paths.append(self.default_prefs_path)

        # Check to see if any service preferences exist for this plug-in
        service_paths = [
            os.path.join(*CONTENTS + ['Services', 'URL']),
            os.path.join(*CONTENTS + ['Search Services']),
            os.path.join(*CONTENTS + ['Related Content Services'])
        ]
        service_json_default = 'ServicePrefs.json'

        for service_path in service_paths:
            for root, dirs, files in os.walk(service_path):
                for name in files:
                    if name == service_json_default:
                        file_paths.append(os.path.join(root, name))
                    elif name.lower() == service_json_default.lower():
                        raise Exception('%s should be named %s' % (name, service_json_default))

        # Iterate over the list of files and try to load prefs.
        for file_path in file_paths:
            if os.path.isfile(file_path):
                try:
                    with open(file_path, mode='r') as f:
                        json_array = json.load(fp=f)
                    prefs_json.extend(json_array)
                    _Log.Debug("Loaded preferences from %s", os.path.split(file_path)[1])
                except Exception:
                    _Log.Exception("Exception loading preferences from %s", os.path.split(file_path)[1])

        # Iterate over the array loaded from the JSON files
        for pref in prefs_json:
            name = pref['id']

            # If a pref object with this name doesn't exist, try to create one
            if name not in self._pref_names:
                # Grab the type, default value, hidden state and label
                pref_type = pref['type']
                pref_secure = 'secure' in pref and (pref['secure'] is True or str(pref['secure']).lower() == 'true')
                pref_hidden = 'hidden' in pref and (pref['hidden'] is True or str(pref['hidden']).lower() == 'true')

                if 'default' in pref:
                    pref_default = pref['default']
                else:
                    pref_default = None
                pref_label = pref['label']

                # Find a suitable class...
                if pref_type == 'text':

                    # Text prefs support options, so parse these too
                    # only known option is 'hidden' ... why use "option" instead of "hidden"?
                    # hidden = hide from UI?
                    if 'option' in pref:
                        pref_option = pref['option'].split(',')
                    else:
                        pref_option = []
                    prefs_dict[name] = _TextPref(label=pref_label,
                                                 default_value=pref_default,
                                                 options=pref_option,
                                                 secure=pref_secure,
                                                 hidden=pref_hidden)

                elif pref_type == 'bool':
                    prefs_dict[name] = _BooleanPref(label=pref_label,
                                                    default_value=pref_default,
                                                    secure=pref_secure,
                                                    hidden=pref_hidden)

                elif pref_type == 'enum':
                    # Enum prefs have a set of values - grab these
                    if 'values' in pref:
                        pref_values = pref['values']
                    else:
                        pref_values = []
                    prefs_dict[name] = _EnumPref(label=pref_label,
                                                 default_value=pref_default,
                                                 values=pref_values,
                                                 secure=pref_secure,
                                                 hidden=pref_hidden)

                # type not found, ignore this preference
                else:
                    raise Exception('This will not be raised in Plex, but I am trying to help you! "%s" pref_type'
                                    'for "%s" not of allowed types ["text", "bool", "enum"].'
                                    % (pref_type, name))

                # Add the name to the names list
                self._pref_names.append(name)

        self._prefs_dict = prefs_dict

    def __getitem__(self, name):
        pref = self._prefs.get(name)

        if pref:
            value = None
            found = False

            # Check for a value stored in the current context
            # raise an exception if a secure preference value couldn't be found
            # pref_values = self._sandbox.context.pref_values.get(self._identifier)
            pref_values = self._prefs_dict
            if pref_values:
                if pref.secure is False or name in pref_values:  # this seems odd... should be and instead of or?
                    value = pref.info_dict('')['value']
                    found = True
                else:
                    raise Exception

            # If we're not on the node, check for a user value.
            if not found and self._user_values:
                value = self._user_values.get(name, pref.default_value)

            return pref.decode_value(value if value else pref.default_value)

        raise KeyError("No preference named '%s' found." % name)


Prefs = _PreferenceSet('test')

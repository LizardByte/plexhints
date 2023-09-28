# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import base64
from future.moves.urllib.parse import quote, quote_plus, unquote, unquote_plus, urlencode, urljoin, parse_qs, parse_qsl
import math
from operator import attrgetter, itemgetter
import os
import random
import re
import six
import string
import sys
import textwrap
from typing import AnyStr, Dict, Iterable, List, Optional, SupportsFloat, Tuple
import unicodedata
import uuid

# lib imports
from bs4 import BeautifulSoup

try:
    xrange
except NameError:
    from past.builtins import range, xrange

# local imports
from plexhints.log_kit import _LogKit

# setup logging
_Log = _LogKit()

# redefine unicode
try:
    unicode
except NameError:
    unicode = str

# (pattern, search, replace) regex english plural rules tuple
_plural_rules = (
    ('[ml]ouse$', '([ml])ouse$', '\\1ice'),
    ('child$', 'child$', 'children'),
    ('booth$', 'booth$', 'booths'),
    ('foot$', 'foot$', 'feet'),
    ('ooth$', 'ooth$', 'eeth'),
    ('l[eo]af$', 'l([eo])af$', 'l\\1aves'),
    ('sis$', 'sis$', 'ses'),
    ('man$', 'man$', 'men'),
    ('ife$', 'ife$', 'ives'),
    ('eau$', 'eau$', 'eaux'),
    ('lf$', 'lf$', 'lves'),
    ('[sxz]$', '$', 'es'),
    ('[^aeioudgkprt]h$', '$', 'es'),
    ('(qu|[^aeiou])y$', 'y$', 'ies'),
    ('$', '$', 's')
)


def _clean_up_string(s):
    # type: (str) -> str
    s = unicode(s)

    s = s.replace('&', 'and')  # replace and symbol
    s = re.sub('[' + string.punctuation + ']', '', s)  # remove punctuation
    s = s.lower()  # make lowercase
    s = re.sub('^(the|a) ', '', s)  # strip leading "the/a"
    s = re.sub('[ ]+', ' ', s).strip()  # fix spaces
    return s


def _levenshtein_distance(first, second):
    # type: (str, str) -> int
    first = _clean_up_string(first)
    second = _clean_up_string(second)

    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for x in range(first_length)]
    for i in range(first_length):
        distance_matrix[i][0] = i
    for j in range(second_length):
        distance_matrix[0][j] = j
    for i in xrange(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution = substitution + 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length - 1][second_length - 1]


def _longest_common_substring(first, second):
    # type: (str, str) -> str
    string_first = _clean_up_string(first)
    string_second = _clean_up_string(second)

    len_first = len(string_first)
    len_second = len(string_second)
    matrix = [[0] * (len_second + 1) for i in xrange(len_first + 1)]
    lcs = set()
    longest = 0
    for i in xrange(len_first):
        for j in xrange(len_second):
            if string_first[i] == string_second[j]:
                value = matrix[i][j] + 1
                matrix[i + 1][j + 1] = value
                if value > longest:
                    longest = value
                    lcs = set()
                if value == longest:
                    lcs.add(string_first[i - value + 1:i + 1])
    if len(lcs) > 0:
        return lcs.pop()
    return ''


def _plural(noun):
    # type: (str) -> str
    for rule in _regex_rules():
        result = rule(noun)
        if result:
            return result


def _regex_rules(rules=_plural_rules):
    # type: (tuple) -> Iterable
    for line in rules:
        pattern, search, replace = line
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)


def _safe_encode(s):
    # type: (str) -> str
    # Ensure input is in bytes format for encoding
    if isinstance(s, str):
        s = s.encode('utf-8')

    encoded_bytes = base64.b64encode(s)

    # If Python 3, decode the bytes to string; then make replacements
    encoded_str = encoded_bytes.decode('utf-8') if isinstance(encoded_bytes, bytes) else encoded_bytes

    return encoded_str.replace('/', '@').replace('+', '*').replace('=', '_')


def _safe_decode(s):
    # type: (str) -> str
    if not isinstance(s, six.text_type):
        s = s.decode('utf-8')

    decoded_bytes = base64.b64decode(s.replace('@', '/').replace('*', '+').replace('_', '=') + '=' * (4 - len(s) % 4))

    if six.PY3:
        return str(decoded_bytes.decode('utf-8'))
    return decoded_bytes


def _url_encode(s):
    # type: (str) -> str
    encoded_str = urlencode({'v': s})
    return encoded_str[2:]


def _version_at_least(version, *components):
    # type: (Optional[str], *any) -> bool
    if version is None:
        return False
    string_parts = version.split('-')[0].split('.')
    int_parts = []
    for part in string_parts:
        try:
            int_parts.append(int(part))
        except Exception:
            int_parts.append(0)
    parts = tuple(int_parts)
    return parts >= tuple(components)


class _StringKit:

    def __init__(self):
        self.LETTERS = string.ascii_letters
        self.LOWERCASE = string.ascii_lowercase
        self.UPPERCASE = string.ascii_uppercase
        self.DIGITS = string.digits
        self.HEX_DIGITS = string.hexdigits
        # string.letters not available in python 3
        self.LETTERS = '{}{}'.format(string.ascii_lowercase, string.ascii_uppercase)
        self.OCT_DIGITS = string.octdigits
        self.PUNCTUATION = string.punctuation
        self.PRINTABLE = string.printable
        self.WHITESPACE = string.whitespace

    def Encode(self, s):
        # type: (str) -> str
        """
        Encodes the given string using the framework's standard encoding (a slight variant on Base64 which ensures
        that the string can be safely used as part of a URL).
        """
        return _safe_encode(s=s)

    def Decode(self, s):
        # type: (str) -> str
        """
        Decodes a string previously encoded using the above function.
        """
        return _safe_decode(s=s)

    def Base64Encode(self, s, with_newlines=False):
        # type: (str, bool) -> str
        """
        Encodes the given string using Base64 encoding.
        """
        # Convert string to bytes for encoding
        if isinstance(s, str):
            s = s.encode('utf-8')

        if with_newlines:
            # Check for Python version and use the appropriate method
            encoded_bytes = base64.encodebytes(s) if hasattr(base64, "encodebytes") else base64.encodestring(s)
        else:
            encoded_bytes = base64.b64encode(s)

        # Convert encoded bytes back to string
        return str(encoded_bytes.decode('utf-8'))

    def Base64Decode(self, s):
        # type: (str) -> str
        """
        Decodes the given Base64-encoded string.
        """
        # Convert string to bytes for decoding
        if isinstance(s, str):
            s = s.encode('utf-8')

        # Check for Python version and use the appropriate method
        decoded_bytes = base64.decodebytes(s) if hasattr(base64, "decodebytes") else base64.decodestring(s)

        # Convert decoded bytes back to string
        return str(decoded_bytes.decode('utf-8'))

    def Quote(self, s, usePlus=False):
        # type: (str, bool) -> str
        """
        Replaces special characters in *s* using the ``%xx`` escape. Letters, digits, and the characters ``'_.-'``
        are never quoted. If *usePlus* is ``True``, spaces are escaped as a plus character instead of ``%20``.
        """
        if usePlus:
            return quote_plus(s)
        else:
            return quote(s)

    def URLEncode(self, s):
        # type: (str) -> str
        return _url_encode(s=s)

    def Unquote(self, s, usePlus=False):
        # type: (str, bool) -> str
        """
        Replace ``%xx`` escapes by their single-character equivalent. If *usePlus* is ``True``, plus characters are
        replaced with spaces.
        """
        if usePlus:
            return unquote_plus(s)
        else:
            return unquote(s)

    def Join(self, words, sep=None):
        # type: (Iterable[AnyStr], AnyStr) -> AnyStr
        try:  # python 2
            return string.join(words, sep)
        except AttributeError:  # python 3
            return sep.join(words)

    def JoinURL(self, base, url, allow_fragments=True):
        # type: (AnyStr, AnyStr, bool) -> AnyStr
        return urljoin(base, url, allow_fragments)

    def StripTags(self, s):
        # type: (AnyStr) -> AnyStr
        """
        Removes HTML tags from a given string.
        """
        return re.sub(r'<[^<>]+>', '', s)

    def DecodeHTMLEntities(self, s):
        # type: (str) -> str
        """
        Converts HTML entities into regular characters (e.g. "&amp;"" => "&")
        """
        soup = BeautifulSoup(s, "html.parser")
        return str(soup.get_text())

    def UUID(self):
        """
        Generates a universally unique identifier (UUID) string. This string is guaranteed to be unique.
        """
        return str(uuid.uuid4())

    def StripDiacritics(self, s):
        # type: (str) -> str
        """
        Removes diacritics from a given string.
        """
        temp = unicode(s)

        u = temp.replace(u"\u00df", u"ss").replace(u"\u1e9e", u"SS")
        nkfd_form = unicodedata.normalize('NFKD', u)
        only_ascii = str(nkfd_form.encode('ASCII', 'ignore').decode())
        return only_ascii

    def Pluralize(self, s):
        # type: (str) -> str
        """
        Attempts to return a pluralized version of the given string (e.g. converts ``boot`` to ``boots``).
        """
        return _plural(noun=s)

    def LevenshteinDistance(self, first, second):
        # type: (str, str) -> int
        """
        Computes the `Levenshtein distance <http://en.wikipedia.org/wiki/Levenshtein_distance>`_ between two given
        strings.
        """
        return _levenshtein_distance(first=first, second=second)

    def LevenshteinRatio(self, first, second):
        # type: (str, str) -> float
        """
        Computes the `Levenshtein ratio (0-1) <http://en.wikipedia.org/wiki/Levenshtein_distance>`_ between two given
        strings.
        """
        if len(first) == 0 or len(second) == 0:
            return 0.0
        else:
            return 1 - (_levenshtein_distance(first=first, second=second) / float(max(len(first), len(second))))

    def LongestCommonSubstring(self, first, second):
        # type: (str, str) -> str
        """
        Returns the longest substring contained within both strings.
        """
        return _longest_common_substring(first=first, second=second)

    def CapitalizeWords(self, s):
        # type: (str) -> str
        return string.capwords(s)

    def ParseQueryString(self, s, keep_blank_vaues=True, strict_parsing=False):
        # type: (str, bool, bool) -> Dict[AnyStr, List[AnyStr]]
        return parse_qs(s, keep_blank_vaues, strict_parsing)  # plex uses cgi.parse.qs instead

    def ParseQueryStringAsList(self, s, keep_blank_vaues=True, strict_parsing=False):
        # type: (str, bool, bool) -> List[Tuple[AnyStr, AnyStr]]
        return parse_qsl(s, int(keep_blank_vaues), strict_parsing)  # plex uses cgi.parse.qsl instead

    def SplitExtension(self, s):
        # type: (AnyStr) -> Tuple[AnyStr, AnyStr]
        return os.path.splitext(s)

    def Dedent(self, s):
        # type: (AnyStr) -> AnyStr
        return textwrap.dedent(s)

    def Clean(self, s, form='NFKD', lang=None, strip_diacritics=False, strip_punctuation=False):
        # type: (AnyStr, str, Optional[str], bool, bool) -> AnyStr

        # Guess at a language-specific encoding, should we need one.
        encoding_map = {'ko': 'cp949'}

        # precompose
        try:
            s = unicodedata.normalize(form, s.decode('utf-8'))
        except Exception:
            try:
                s = unicodedata.normalize(form, s.decode(sys.getdefaultencoding()))
            except Exception:
                try:
                    s = unicodedata.normalize(form, s.decode(sys.getfilesystemencoding()))
                except Exception:
                    try:
                        s = unicodedata.normalize(form, s.decode('utf-16'))
                    except Exception:
                        try:
                            s = unicodedata.normalize(form, s.decode(encoding_map.get(lang, 'ISO-8859-1')))
                        except Exception:
                            try:
                                s = unicodedata.normalize(form, s)
                            except Exception as e:
                                _Log.Exception(type(e).__name__ + ' exception precomposing: ' + str(e))

        # strip control characters
        s = u''.join([c for c in s if not unicodedata.category(c).startswith('C')])

        # strip punctuation
        if strip_punctuation:
            s = u''.join([c for c in s if not unicodedata.category(c).startswith('P')])

        # strip diacritics
        if strip_diacritics:
            s = u''.join([c for c in s if not unicodedata.combining(c)])

        return s


class _UtilKit:
    def __init__(self):
        pass

    def Floor(self, x):
        # type: (SupportsFloat) -> float
        return math.floor(x)

    def Ceiling(self, x):
        # type: (SupportsFloat) -> float
        return math.ceil(x)

    def VersionAtLeast(self, version_string, *components):
        # type: (Optional[str], *any) -> bool
        return _version_at_least(version_string, *components)

    def ListSortedByKey(self, l, key):  # noqa: E741  # cannot rename variables
        # type: (list, any) -> list
        return sorted(l, key=itemgetter(key))

    def ListSortedByAttr(self, l, attr):  # noqa: E741  # cannot rename variables
        # type: (list, str) -> list
        return sorted(l, key=attrgetter(attr))

    def SortListByKey(self, l, key):  # noqa: E741  # cannot rename variables
        # type: (list, any) -> None
        l.sort(key=itemgetter(key))

    def SortListByAttr(self, l, attr):  # noqa: E741  # cannot rename variables
        # type: (list, str) -> None
        l.sort(key=attrgetter(attr))

    def LevenshteinDistance(self, first, second):
        # type: (str, str) -> int
        return _levenshtein_distance(first, second)

    def LongestCommonSubstring(self, first, second):
        # type: (str, str) -> str
        return _longest_common_substring(first, second)

    def Random(self):
        # type: () -> float
        """
        Returns a random number between 0 and 1.

        Returns
        -------
        float
        """
        return random.random()

    def RandomInt(self, a, b):
        # type: (int, int) -> int
        """
        Returns a random integer *N* such that ``a <= N <= b``.
        """
        return random.randint(a, b)

    def RandomItemFromList(self, l):  # noqa: E741  # cannot rename variables
        # type: (list) -> any
        """
        Returns a random item selected from the given list.
        """
        return l[random.randint(0, len(l) - 1)]

    def RandomChoice(self, l):  # noqa: E741  # cannot rename variables
        # type: (list) -> any
        return random.choice(l)

    def RandomSample(self, l, count):  # noqa: E741  # cannot rename variables
        # type: (list, int) -> list
        return random.sample(l, count)


String = _StringKit()
Util = _UtilKit()

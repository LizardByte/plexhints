# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import math
from operator import attrgetter, itemgetter
import random
import re
import string
from typing import Optional, SupportsFloat

# lib imports
try:
    xrange
except NameError:
    from past.builtins import range, xrange


def clean_up_string(s):
    # type: (str) -> str
    try:
        s = unicode(s)
    except NameError:  # `unicode` is not available in python 3.5+
        pass

    s = s.replace('&', 'and')  # replace and symbol
    s = re.sub('[' + string.punctuation + ']', '', s)  # remove punctuation
    s = s.lower()  # make lowercase
    s = re.sub('^(the|a) ', '', s)  # strip leading "the/a"
    s = re.sub('[ ]+', ' ', s).strip()  # fix spaces
    return s


def levenshtein_distance(first, second):
    # type: (str, str) -> int
    first = clean_up_string(first)
    second = clean_up_string(second)

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


def longest_common_substring(first, second):
    # type: (str, str) -> str
    string_first = clean_up_string(first)
    string_second = clean_up_string(second)

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


def version_at_least(version, *components):
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


class UtilKit:
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
        return version_at_least(version_string, *components)

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
        return levenshtein_distance(first, second)

    def LongestCommonSubstring(self, first, second):
        # type: (str, str) -> str
        return longest_common_substring(first, second)

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

# -*- coding: utf-8 -*-

# lib imports
import pytest

# local imports
from plexhints import util_kit


@pytest.mark.parametrize('lead_word', ['A', 'The'])
def test_clean_up_string(lead_word):
    test_string = '{} test string & it has some special characters... !#*+, & double  spaces'.format(lead_word)
    expected_string = 'test string and it has some special characters and double spaces'
    assert util_kit._clean_up_string(test_string) == expected_string


def test_levenshtein_distance():
    assert util_kit._levenshtein_distance(first='test', second='test') == 0
    assert util_kit._levenshtein_distance(first='test', second='test1') == 1
    assert util_kit._levenshtein_distance(first='test', second='test12') == 2


def test_longest_common_substring():
    first = 'This is a long string with a lot of words in it'
    second = 'This is a longer string with a lot of words in it'
    assert util_kit._longest_common_substring(first=first, second=second) == ' string with a lot of words in it'


def test_plural():
    assert util_kit._plural('test') == 'tests'
    assert util_kit._plural('mouse') == 'mice'
    assert util_kit._plural('child') == 'children'
    assert util_kit._plural('person') == 'persons'
    assert util_kit._plural('foot') == 'feet'
    assert util_kit._plural('foundry') == 'foundries'


def test_regex_rules():
    # test this function
    # def _regex_rules(rules=_plural_rules):
    #     # type: (tuple) -> Iterable
    #     for line in rules:
    #         pattern, search, replace = line
    #         yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)

    # test the function
    regex_rules = util_kit._regex_rules()

    checks = (
        'mouse',
        'grandchild',
        'booth',
        'foot',
        'booth',
        'loaf',
        'sis',
        'woman',
        'wife',
        'eau',
        'elf',
        'ex',
        'bush',
        'foundry',
        'test',
    )
    for check in checks:
        # test the rules
        rule = next(regex_rules)
        assert rule(check) is not None


def test_safe_encode():
    # test base 64 encoding and replacement of some characters
    # / -> @
    # + -> *
    # = -> _
    test_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    expected_string = 'cHJvdG9jb2w6Ly90ZXN0L3BhdGgvdG8vZmlsZS5leHQrP3BhcmFtMT12YWx1ZTEmcGFyYW0yPXZhbHVlMg__'
    assert util_kit._safe_encode(test_string) == expected_string


def test_safe_decode():
    # test base 64 decoding and replacement of some characters
    # @ -> /
    # * -> +
    # _ -> =
    test_string = 'cHJvdG9jb2w6Ly90ZXN0L3BhdGgvdG8vZmlsZS5leHQrP3BhcmFtMT12YWx1ZTEmcGFyYW0yPXZhbHVlMg__'
    expected_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    assert util_kit._safe_decode(test_string) == expected_string


def test_url_encode():
    # test url encoding
    test_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    expected_string = 'protocol%3A%2F%2Ftest%2Fpath%2Fto%2Ffile.ext%2B%3Fparam1%3Dvalue1%26param2%3Dvalue2'
    assert util_kit._url_encode(test_string) == expected_string


def test_version_at_least():
    version = '1.2.3'

    # test this functino
    # def _version_at_least(version, *components):
    #   # type: (Optional[str], *any) -> bool
    assert util_kit._version_at_least(version, 1, 2, 3)
    assert util_kit._version_at_least(version, 1, 2)
    assert util_kit._version_at_least(version, 1)
    assert util_kit._version_at_least(version, 0)
    assert util_kit._version_at_least(version, 1, 2, 3, 4) is False
    assert util_kit._version_at_least(version, 1, 2, 4) is False
    assert util_kit._version_at_least(version, 1, 3) is False
    assert util_kit._version_at_least(version, 2) is False


@pytest.fixture(scope='function')
def string_kit():
    return util_kit._StringKit()


def test_string_kit_encode(string_kit):
    # safe encode
    test_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    expected_string = 'cHJvdG9jb2w6Ly90ZXN0L3BhdGgvdG8vZmlsZS5leHQrP3BhcmFtMT12YWx1ZTEmcGFyYW0yPXZhbHVlMg__'
    assert string_kit.Encode(test_string) == expected_string


def test_string_kit_decode(string_kit):
    # safe decode
    test_string = 'cHJvdG9jb2w6Ly90ZXN0L3BhdGgvdG8vZmlsZS5leHQrP3BhcmFtMT12YWx1ZTEmcGFyYW0yPXZhbHVlMg__'
    expected_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    assert string_kit.Decode(test_string) == expected_string


@pytest.mark.parametrize('with_newlines, expected_string', [
    (True, 'cHJvdG9jb2w6Ly90ZXN0L3BhdGgvdG8vZmlsZS5leHQrP3BhcmFtMT12YWx1ZTEmcGFyYW0yPXZh\nbHVlMg==\n'),
    (False, 'cHJvdG9jb2w6Ly90ZXN0L3BhdGgvdG8vZmlsZS5leHQrP3BhcmFtMT12YWx1ZTEmcGFyYW0yPXZhbHVlMg=='),
])
def test_string_kit_base64_encode(string_kit, expected_string, with_newlines):
    # base 64 encode
    test_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    assert string_kit.Base64Encode(s=test_string, with_newlines=with_newlines) == expected_string


def test_string_kit_base64_decode(string_kit):
    # base 64 decode
    test_string = 'cHJvdG9jb2w6Ly90ZXN0L3BhdGgvdG8vZmlsZS5leHQrP3BhcmFtMT12YWx1ZTEmcGFyYW0yPXZhbHVlMg=='
    expected_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    assert string_kit.Base64Decode(test_string) == expected_string


@pytest.mark.parametrize('use_plus', [True, False])
def test_string_kit_quote(string_kit, use_plus):
    # quote
    test_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    expected_string_plus_false = 'protocol%3A//test/path/to/file.ext%2B%3Fparam1%3Dvalue1%26param2%3Dvalue2'
    expected_string_plus_true = 'protocol%3A%2F%2Ftest%2Fpath%2Fto%2Ffile.ext%2B%3Fparam1%3Dvalue1%26param2%3Dvalue2'

    if use_plus:
        assert string_kit.Quote(test_string, usePlus=use_plus) == expected_string_plus_true
    else:
        assert string_kit.Quote(test_string, usePlus=use_plus) == expected_string_plus_false


def test_string_kit_url_encode(string_kit):
    # url encode
    test_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'
    expected_string = 'protocol%3A%2F%2Ftest%2Fpath%2Fto%2Ffile.ext%2B%3Fparam1%3Dvalue1%26param2%3Dvalue2'
    assert string_kit.URLEncode(test_string) == expected_string


@pytest.mark.parametrize('use_plus', [True, False])
def test_string_kit_unquote(string_kit, use_plus):
    # unquote
    test_string_plus_false = 'protocol%3A//test/path/to/file.ext%2B%3Fparam1%3Dvalue1%26param2%3Dvalue2'
    test_string_plus_true = 'protocol%3A%2F%2Ftest%2Fpath%2Fto%2Ffile.ext%2B%3Fparam1%3Dvalue1%26param2%3Dvalue2'
    expected_string = 'protocol://test/path/to/file.ext+?param1=value1&param2=value2'

    if use_plus:
        assert string_kit.Unquote(test_string_plus_true, usePlus=use_plus) == expected_string
    else:
        assert string_kit.Unquote(test_string_plus_false, usePlus=use_plus) == expected_string


@pytest.mark.parametrize('separator', [' ', '_', '-'])
def test_string_kit_join(string_kit, separator):
    # join
    words = ['this', 'is', 'a', 'test']
    expected_string = 'this{s}is{s}a{s}test'.format(s=separator)
    assert string_kit.Join(words, sep=separator) == expected_string


@pytest.mark.parametrize('url, allow_fragments, expected_url', [
    ('FAQ.html', True, 'https://example.com/FAQ.html'),
    ('FAQ.html', False, 'https://example.com/FAQ.html'),
    ('FAQ.html#newFragment', True, 'https://example.com/FAQ.html#newFragment'),
    ('FAQ.html#newFragment', False, 'https://example.com/FAQ.html#newFragment'),
])
def test_string_kit_join_url(string_kit, url, allow_fragments, expected_url):
    base_url = 'https://example.com/base.html#baseFragment'

    joined_url = string_kit.JoinURL(base=base_url, url=url, allow_fragments=allow_fragments)
    assert joined_url == expected_url


def test_string_kit_strip_tags(string_kit):
    # strip tags
    test_string = '<p>test string</p>'
    expected_string = 'test string'
    assert string_kit.StripTags(test_string) == expected_string


def test_string_kit_decode_html_entities(string_kit):
    # decode html entities
    test_string = '&lt;p&gt;test string&lt;/p&gt;'
    expected_string = '<p>test string</p>'
    assert string_kit.DecodeHTMLEntities(test_string) == expected_string


def test_string_kit_uuid(string_kit):
    # test we get uuid4
    unique_id = string_kit.UUID()
    assert len(unique_id) == 36
    assert unique_id.count('-') == 4


def test_string_kit_strip_diacritics(string_kit):
    # test removing diacritics from a given string
    test_string = 'tést strïng'
    expected_string = 'test string'
    assert string_kit.StripDiacritics(test_string) == expected_string


def test_string_kit_pluralize(string_kit):
    # test pluralizing a given string
    test_string = 'test'
    expected_string = 'tests'
    assert string_kit.Pluralize(test_string) == expected_string


def test_string_kit_levenshtein_distance(string_kit):
    # test levenshtein distance
    assert string_kit.LevenshteinDistance(first='test', second='test') == 0
    assert string_kit.LevenshteinDistance(first='test', second='test1') == 1
    assert string_kit.LevenshteinDistance(first='test', second='test12') == 2


def test_string_kit_longest_common_substring(string_kit):
    # test longest common substring
    first = 'This is a long string with a lot of words in it'
    second = 'This is a longer string with a lot of words in it'
    assert string_kit.LongestCommonSubstring(first=first, second=second) == ' string with a lot of words in it'


@pytest.mark.parametrize('word', ['test', 'mouse', 'child', 'person', 'foot', 'foundry'])
def test_string_kit_capitalize_words(string_kit, word):
    # test capitalizing words
    assert string_kit.CapitalizeWords(word) == word.capitalize()


def test_string_kit_parse_query_string(string_kit):
    # test parsing a query string
    test_string = 'param1=value1&param2=value2'
    expected_dict = {'param1': ['value1'], 'param2': ['value2']}
    assert string_kit.ParseQueryString(test_string) == expected_dict


def test_string_kit_parse_query_string_as_list(string_kit):
    # test parsing a query string as a list
    test_string = 'param1=value1&param2=value2'
    expected_list = [('param1', 'value1'), ('param2', 'value2')]
    assert string_kit.ParseQueryStringAsList(test_string) == expected_list


def test_string_kit_split_extension(string_kit):
    # test splitting an extension from a file name
    test_string = 'test.ext'
    expected_tuple = ('test', '.ext')
    assert string_kit.SplitExtension(test_string) == expected_tuple


def test_string_kit_dedent(string_kit):
    # test dedenting a string
    test_string = '    test string'
    expected_string = 'test string'
    assert string_kit.Dedent(test_string) == expected_string


def test_string_kit_clean(string_kit):
    # test clean

    # string with control characters, punctuation to be stripped, diacritics to be stripped
    test_string = 'tèst strïng!'
    expected_string = 'test string'
    assert string_kit.Clean(test_string, strip_diacritics=True, strip_punctuation=True) == expected_string


@pytest.fixture(scope='function')
def util_kit_object():
    return util_kit._UtilKit()


def test_util_kit_floor(util_kit_object):
    # test floor
    assert util_kit_object.Floor(1.5) == 1
    assert util_kit_object.Floor(1.4) == 1
    assert util_kit_object.Floor(1.6) == 1


def test_util_kit_ceiling(util_kit_object):
    # test ceiling
    assert util_kit_object.Ceiling(1.5) == 2
    assert util_kit_object.Ceiling(1.4) == 2
    assert util_kit_object.Ceiling(1.6) == 2


def test_util_kit_version_at_least(util_kit_object):
    # test version at least
    version = '1.2.3'
    assert util_kit_object.VersionAtLeast(version, 1, 2, 3)
    assert util_kit_object.VersionAtLeast(version, 1, 2)
    assert util_kit_object.VersionAtLeast(version, 1)
    assert util_kit_object.VersionAtLeast(version, 0)
    assert util_kit_object.VersionAtLeast(version, 1, 2, 3, 4) is False
    assert util_kit_object.VersionAtLeast(version, 1, 2, 4) is False
    assert util_kit_object.VersionAtLeast(version, 1, 3) is False
    assert util_kit_object.VersionAtLeast(version, 2) is False


def test_util_kit_list_sorted_by_key(util_kit_object):
    # test sorting a list of dictionaries by a given key
    test_list = [{'key': 2}, {'key': 1}, {'key': 3}]
    expected_list = [{'key': 1}, {'key': 2}, {'key': 3}]
    assert util_kit_object.ListSortedByKey(test_list, 'key') == expected_list


def test_util_kit_list_sorted_by_attr(util_kit_object):
    # test sorting a list of objects by a given attribute
    class TestObject(object):
        def __init__(self, key):
            self.key = key

    a = TestObject(1)
    b = TestObject(2)
    c = TestObject(3)

    test_list = [b, c, a]
    expected_list = [a, b, c]
    assert util_kit_object.ListSortedByAttr(test_list, 'key') == expected_list


def test_util_kit_levenshtein_distance(util_kit_object):
    # test levenshtein distance
    assert util_kit_object.LevenshteinDistance(first='test', second='test') == 0
    assert util_kit_object.LevenshteinDistance(first='test', second='test1') == 1
    assert util_kit_object.LevenshteinDistance(first='test', second='test12') == 2


def test_util_kit_longest_common_substring(util_kit_object):
    # test longest common substring
    first = 'This is a long string with a lot of words in it'
    second = 'This is a longer string with a lot of words in it'
    assert util_kit_object.LongestCommonSubstring(first=first, second=second) == ' string with a lot of words in it'


def test_util_kit_random(util_kit_object):
    # test that we get a random number
    for _ in range(1000):
        random_number = util_kit_object.Random()
        assert random_number >= 0
        assert isinstance(random_number, float)


@pytest.mark.parametrize('range_start, range_end', [(1, 10), (10, 100), (100, 1000)])
def test_util_kit_random_int(util_kit_object, range_start, range_end):
    # test that we get a random integer
    for _ in range(1000):
        random_int = util_kit_object.RandomInt(a=range_start, b=range_end)
        assert range_start <= random_int <= range_end
        assert isinstance(random_int, int)


def test_util_kit_random_item_from_list(util_kit_object):
    # test that we get a random item from a list
    test_list = []
    for i in range(1000):
        test_list.append(i)
    for _ in range(1000):
        random_item = util_kit_object.RandomItemFromList(test_list)
        assert random_item in test_list


def test_util_kit_random_choice(util_kit_object):
    test_list = [
        'yes',
        'no',
        'maybe',
    ]
    for _ in range(1000):
        random_choice = util_kit_object.RandomChoice(test_list)
        assert random_choice in test_list


def test_util_kit_random_sample(util_kit_object):
    test_list = [
        'yes',
        'no',
        'maybe',
    ]
    for _ in range(1000):
        random_sample = util_kit_object.RandomSample(l=test_list, count=2)
        assert len(random_sample) == 2
        assert random_sample[0] in test_list
        assert random_sample[1] in test_list

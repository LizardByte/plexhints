# -*- coding: utf-8 -*-

# standard imports
import os

# lib imports
import pytest

# local imports
from plexhints import resource_kit

LINE_ENDING = '\r\n' if os.name == 'nt' else '\n'


@pytest.mark.parametrize('binary', [False, True])
def test_load(binary, data_dir):
    contents = resource_kit.__load(path=os.path.join(data_dir, 'dummy-data.txt'), binary=binary)
    assert isinstance(contents, bytes) if binary else isinstance(contents, str)

    if binary:
        # line ending depends on the OS we're on
        # encode the string back to bytes
        assert contents == 'Hello, World!{}'.format(LINE_ENDING).encode('utf-8')
    else:
        assert contents == 'Hello, World!\n'

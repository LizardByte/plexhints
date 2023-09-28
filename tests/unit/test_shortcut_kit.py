# -*- coding: utf-8 -*-

# lib imports
import pytest

# local imports
from plexhints import shortcut_kit


@pytest.mark.parametrize(
    'shortcuts', [
        ('L', shortcut_kit.Locale.LocalStringWithFormat),
        ('E', shortcut_kit.String.Encode),
        ('D', shortcut_kit.String.Decode),
        ('R', shortcut_kit.Resource.ExternalPath),
        ('S', shortcut_kit.Resource.SharedExternalPath),
    ]
)
def test_shortcut_kit(shortcuts):
    shortcut, method = shortcuts
    assert hasattr(shortcut_kit, shortcut)
    assert getattr(shortcut_kit, shortcut) == method

# -*- coding: utf-8 -*-

# lib imports
import pytest

# local imports
from plexhints import exception_kit


@pytest.fixture(scope='session')
def exceptions():
    return exception_kit._Exceptions()


def test_exceptions(exceptions):
    exception_list = [
        exceptions.FrameworkException(),
        exceptions.UnauthorizedException(),
        exceptions.BadRequestException(),
        exceptions.AttributeException(),
        exceptions.RedirectError(code=1000, headers={'pytest': 'true'}),
        exceptions.PlexError(code=2000, status='Fake PlexError'),
        exceptions.PlexNonCriticalError(code=2000, status='Fake PlexNotCriticalError'),
        exceptions.MediaNotAvailable(),
        exceptions.MediaExpired(),
        exceptions.LiveMediaNotStarted(),
        exceptions.MediaNotAuthorized(),
        exceptions.MediaGeoblocked(),
        exceptions.StreamLimitExceeded(),
        exceptions.AttributeTypeMismatch(status='AttributeTypeError'),
        exceptions.ContextException(status='ContextError'),
        exceptions.APIException(status='APIError'),
        exceptions.NonCriticalArgumentException(status='NonCriticalArgumentError'),
    ]
    for exception in exception_list:
        with pytest.raises(exception.__class__):
            raise exception

# -*- coding: utf-8 -*-
# standard imports
from functools import partial
import os
import re
import sys
import time

# lib imports
import plexapi
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexhints.core_kit import PLUGIN_LOGS_PATH
import pytest
import requests

# add Contents directory to the system path
if os.path.isdir('Contents'):
    sys.path.append('Contents')

    # local imports
    from Code import constants
else:
    raise Exception('Contents directory not found')

# plex server setup
SERVER_BASEURL = plexapi.CONFIG.get("auth.server_baseurl")


def _wait_for_file(f):
    # type: (str) -> None
    """Wait for a file to exist with a timeout."""
    attempts = 0
    max_attempts = 120
    while not os.path.isfile(f) and attempts < max_attempts:
        time.sleep(1)
        attempts += 1
    assert attempts < max_attempts, "File not found after {}s".format(attempts)


# plex server fixtures
@pytest.fixture(scope="session")
def plugin_logs():
    # list contents of the plugin logs directory
    plugin_logs = os.listdir(PLUGIN_LOGS_PATH)

    yield plugin_logs


# plex server fixtures
@pytest.fixture(scope="session")
def plugin_log_file():
    # the primary plugin log file
    plugin_log_file = os.path.join(PLUGIN_LOGS_PATH, "{}.log".format(constants.plugin_identifier))

    # wait for the plugin log file to exist
    _wait_for_file(plugin_log_file)

    yield plugin_log_file


@pytest.fixture(scope="session")
def plex_token(plugin_log_file):
    # get all the lines in the plugin log file
    with open(plugin_log_file, 'r') as f:
        lines = f.readlines()

    print('lines: {}'.format(lines))

    # Compile the regex pattern
    plex_token_pattern = re.compile(r'plex-x-token: ([a-z0-9]+)')

    plex_token = None
    for line in lines:
        match = plex_token_pattern.search(line)
        if match:
            plex_token = match.group(1)
            break

    yield plex_token


@pytest.fixture(scope="session")
def sess():
    session = requests.Session()
    session.request = partial(session.request, timeout=120)
    return session


@pytest.fixture(scope="session")
def plex(request, plex_token, sess):
    assert SERVER_BASEURL, "Required SERVER_BASEURL not specified."
    token = plex_token if plex_token else MyPlexAccount(session=sess).authenticationToken
    return PlexServer(SERVER_BASEURL, token, session=sess)


@pytest.fixture(scope="session")
def plex2(request, sess):
    assert SERVER_BASEURL, "Required SERVER_BASEURL not specified."
    token = None
    return PlexServer(SERVER_BASEURL, token, session=sess)


@pytest.fixture()
def movies_new_section(plex):
    section = plex.library.section("Movies")
    return section


@pytest.fixture()
def movies_imdb_section(plex):
    section = plex.library.section("Movies-imdb")
    return section


@pytest.fixture()
def movies_themoviedb_section(plex):
    movies = plex.library.section("Movies-tmdb")
    return movies


@pytest.fixture()
def tv_shows_section(plex):
    section = plex.library.section("TV Shows")
    return section


@pytest.fixture()
def music_section(plex):
    section = plex.library.section("Music")
    return section


@pytest.fixture()
def photo_section(plex):
    section = plex.library.section("Photos")
    return section

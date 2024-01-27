# -*- coding: utf-8 -*-
# standard imports
from functools import partial
import os
import re
import shutil
import sys
import time
from threading import Thread

# conditional imports
try:
    from http.server import SimpleHTTPRequestHandler
    import socketserver
except ImportError:  # Python 2
    from BaseHTTPServer import SimpleHTTPRequestHandler
    import SocketServer as socketserver

# lib imports
import plexapi
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
import pytest
import requests

# local imports
import plexhints

# add Contents directory to the system path
if os.path.isdir('Contents'):
    sys.path.append('Contents')

    # plex plugin imports
    from Code import constants
else:
    raise Exception('Contents directory not found')

# plex server setup
SERVER_BASEURL = plexapi.CONFIG.get("auth.server_baseurl")

# data directory setup
DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')
TEMP_DIRECTORY = os.path.join(os.getcwd(), 'plexhints-tests-temp')


def _wait_for_file(f):
    # type: (str) -> None
    """Wait for a file to exist with a timeout."""
    attempts = 0
    max_attempts = 120
    while not os.path.isfile(f) and attempts < max_attempts:
        time.sleep(1)
        attempts += 1
    assert attempts < max_attempts, "File not found after {}s".format(attempts)


@pytest.fixture(scope="function")
def elevated_policy():
    plexhints.ELEVATED_POLICY = True
    yield


@pytest.fixture(scope="function")
def non_elevated_policy():
    plexhints.ELEVATED_POLICY = False
    yield


# plex server fixtures... test plexhints.bundle CI plugin and GitHub Action are working correctly
@pytest.fixture(scope="session")
def plugin_logs():
    # list contents of the plugin logs directory
    plugin_logs = os.listdir(os.environ['PLEX_PLUGIN_LOG_PATH'])

    yield plugin_logs


@pytest.fixture(scope="session")
def plugin_log_file():
    # the primary plugin log file
    plugin_log_file = os.path.join(os.environ['PLEX_PLUGIN_LOG_PATH'], "{}.log".format(constants.plugin_identifier))

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
def tv_shows_tmdb_section(plex):
    section = plex.library.section("TV Shows-tmdb")
    return section


@pytest.fixture()
def tv_shows_tvdb_section(plex):
    section = plex.library.section("TV Shows-tvdb")
    return section


@pytest.fixture()
def music_section(plex):
    section = plex.library.section("Music")
    return section


@pytest.fixture()
def photo_section(plex):
    section = plex.library.section("Photos")
    return section


@pytest.fixture(scope='session')
def data_dir():
    return DATA_DIRECTORY


@pytest.fixture(scope='session')
def temp_dir():
    yield TEMP_DIRECTORY

    # cleanup
    if os.path.isdir(TEMP_DIRECTORY):
        shutil.rmtree(TEMP_DIRECTORY)


class Handler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.root_dir = DATA_DIRECTORY
        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def translate_path(self, path):
        """This method returns the filesystem path for the served files."""
        # Here, we override the method to serve files from a custom directory.
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.root_dir, relpath)
        return fullpath


@pytest.fixture(scope='session')
def http_server():
    httpd = socketserver.TCPServer(("", 8000), Handler)
    server_thread = Thread(target=httpd.serve_forever)
    server_thread.start()

    yield 'http://localhost:8000/{}'

    httpd.shutdown()
    server_thread.join()

# -*- coding: utf-8 -*-
# standard imports
import os


def test_plugin_los(plugin_logs):
    print('plugin_logs: {}'.format(plugin_logs))
    assert plugin_logs, "No plugin logs found"


def test_plugin_log_file(plugin_log_file):
    assert os.path.isfile(plugin_log_file), "Plugin log file not found: {}".format(plugin_log_file)


def test_plugin_log_file_exceptions(plugin_log_file):
    # get all the lines in the plugin log file
    with open(plugin_log_file, 'r') as f:
        lines = f.readlines()

    critical_exceptions = []
    for line in lines:
        if ') :  CRITICAL (' in line:
            critical_exceptions.append(line)

    assert len(critical_exceptions) <= 1, "Too many exceptions logged to plugin log file"

    for exception in critical_exceptions:
        # every plugin will have this exception
        assert exception.endswith('Exception getting hosted resource hashes (most recent call last):\n'), (
            "Unexpected exception: {}".format(exception))


def test_plugin_log_token_exists(plex_token):
    assert plex_token, "No token found in plugin log file"


def test_plex_token(plex):
    headers = plex._headers()
    assert "X-Plex-Token" in headers
    assert len(headers["X-Plex-Token"]) >= 1


def test_plex2_token(plex2):
    headers = plex2._headers()
    assert "X-Plex-Token" not in headers

# -*- coding: utf-8 -*-
# standard imports
import os

# local imports
import plexhints.const


def test_plexhints_version():
    # parse the changelog file
    changelog_file_path = os.path.join(os.getcwd(), 'CHANGELOG.md')
    with open(changelog_file_path, 'r') as f:
        changelog = f.readlines()

    # get the version from the changelog... ## [major.minor.patch] - yyyy-mm-dd
    changelog_version = None
    for line in changelog:
        if line.startswith('## ['):
            changelog_version = line.split('[', 1)[1].split(']', 1)[0]
            break

    assert plexhints.const.__version__ == changelog_version, "Changelog version does not match plexhints version"

    # ensure there is a url to the version
    accepted_line = '[{v}]: https://github.com/lizardbyte/plexhints/releases/tag/v{v}\n'.format(v=changelog_version)
    found_url = False
    for line in changelog:
        if line == accepted_line:
            found_url = True
            break
    assert found_url, "Changelog version does not have a valid url, should be: {}".format(accepted_line)

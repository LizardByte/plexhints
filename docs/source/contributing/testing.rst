:github_url: https://github.com/LizardByte/plexhints/tree/nightly/docs/source/contributing/testing.rst

Testing
=======

Flake8
------
Plexhints uses `Flake8 <https://pypi.org/project/flake8/>`__ for enforcing consistent code styling. Flake8 is included
in the ``requirements-dev.txt``.

The config file for flake8 is ``.flake8``. This is already included in the root of the repo and should not be modified.

Test with Flake8
   .. code-block:: bash

      python -m flake8

Sphinx
------
Plexhints uses `Sphinx <https://www.sphinx-doc.org/en/master/>`__ for documentation building. Sphinx is included
in the ``requirements-dev.txt``.

Plexhints follows `numpydoc <https://numpydoc.readthedocs.io/en/latest/format.html>`__ styling and formatting in
docstrings. This will be tested when building the docs. `numpydoc` is included in the ``requirements-dev.txt``.

The config file for Sphinx is ``docs/source/conf.py``. This is already included in the root of the repo and should not
be modified.

Test with Sphinx
   .. code-block:: bash

      cd docs
      make html

   Alternatively

   .. code-block:: bash

      cd docs
      sphinx-build -b html source build

Lint with rstcheck
   .. code-block:: bash

      rstcheck -r .

pytest
------
Plexhints uses `pytest <https://pypi.org/project/pytest/>`__ for unit testing. pytest is included in the
``requirements-dev.txt``.

No config file is required for pytest, but pytest relies on a rather specific environment.
Plex Media Server must be installed as well as the following environment variables being set.

- ``PLEX_PLUGIN_LOG_PATH`` - See `Plex Plugin Logs <https://support.plex.tv/articles/201106148-channel-log-files/>`__
- ``PLEXAPI_AUTH_SERVER_BASEURL`` - Normally ``http://127.0.0.1:32400``

Additionally, the ``plexhints.bundle`` must be installed in the Plex Media Server plugins directory.

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         mkdir -p ./plexhints.bundle/Contents
         cp -r ./Contents/. ./plexhints.bundle/Contents

   .. group-tab:: macOS

      .. code-block:: bash

         mkdir -p ./plexhints.bundle/Contents
         cp -r ./Contents/. ./plexhints.bundle/Contents

   .. group-tab:: Windows

      .. code-block:: batch

         mkdir "plexhints.bundle"
         xcopy /E /I "Contents" "plexhints.bundle\Contents"


.. attention::
   A locally installed Plex server is required to run some of the tests. The server must be running locally so that the
   plugin logs can be parsed for exceptions. It is not recommended to run the tests against a production server.

A script is provided that allows you to prepare the Plex server for testing. Use the help argument to see the options.

Bootstrap the Plex server for testing
   .. code-block:: bash

      python scripts/plex_bootstraptest.py --help

Test with pytest
   .. code-block:: bash

      python -m pytest

.. tip::
   Due to the complexity of setting up the environment for testing, it is recommended to run the tests in GitHub
   Actions. This will ensure that the tests are run in a clean environment and will not be affected by any local
   changes.

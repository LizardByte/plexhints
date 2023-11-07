:github_url: https://github.com/LizardByte/plexhints/tree/nightly/docs/source/about/github_action.rst

GitHub Action
=============
A GitHub Action is provided to automate installation and preparation of a Plex Media Server in a CI/CD pipeline.

The action does the following:

1. Installs the latest Plex Media Server for the target platform.
2. Installs any specified plugins to the Plex Media Server.
3. Collects the Plex Media Server authentication token.
4. Provides useful output variables for use in subsequent steps.

Bootstrap Plex server
---------------------

Inputs
^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Default
     - Required
   * - ``accept_eula``
     - Accept Plex's EULA.
     - ``false``
     - false
   * - ``additional_server_queries_put``
     - Space separated list of additional PUT requests to send to the server. The requests are sent before the
       library sections are created. You can use this to enable third party metadata agents, as an example.
       e.g. `/system/agents/com.plexapp.agents.imdb/config/1?order=com.plexapp.agents.imdb%2C<my_movie_agent>`
     - ``""``
     - false
   * - ``bootstrap_timeout``
     - Timeout for each step of bootstrap, in seconds.
     - ``540``
     - false
   * - ``docker_tag``
     - Docker image to install. Only used when ``use_docker`` is ``true``.
     - ``latest``
     - false
   * - ``expose_plex_data_files_for_docker``
     - When using docker, expose the Plex Media Server application data files to the remainder of your workflow at
       ``${{ github.workspace }}/plex``.
     - ``false``
     - false
   * - ``language``
     - Language to set inside Plex.
     - ``en-US.UTF-8``
     - false
   * - ``plugin_bundles_to_install``
     - Space separated list of plugin bundles to install. Provide the relative or absolute path to the bundle.
     - ``""``
     - false
   * - ``timezone``
     - Timezone to set inside Plex.
     - ``UTC``
     - false
   * - ``use_docker``
     - Use Docker to run Plex Media Server. This is only supported on Linux.
     - ``false``
     - false
   * - ``without_movies``
     - Do not create a Movies library (new agent).
     - ``false``
     - false
   * - ``without_movies_imdb``
     - Do not create a Movies library (IMDB agent).
     - ``false``
     - false
   * - ``without_movies_tmdb``
     - Do not create a Movies library (TMDB agent).
     - ``false``
     - false
   * - ``without_music``
     - Do not create a Music library.
     - ``false``
     - false
   * - ``without_photos``
     - Do not create a Photos library.
     - ``false``
     - false
   * - ``without_shows``
     - Do not create a TV Shows library.
     - ``false``
     - false

Outputs
^^^^^^^

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - ``PLEXTOKEN``
     - The Plex Media Server authentication token.
   * - ``PLEX_APP_DATA_PATH``
     - The path to the Plex Media Server application data.
   * - ``PLEX_PLUGIN_LOG_PATH``
     - The path to the Plex Media Server plugin logs.
   * - ``PLEX_PLUGIN_PATH``
     - The path to the Plex Media Server plugins.
   * - ``PLEX_SERVER_BASEURL``
     - The base URL of the Plex Media Server.

Examples
--------

Basic usage
^^^^^^^^^^^
.. code-block:: yaml

   - name: Bootstrap Plex server
     id: bootstrap
     uses: LizardByte/plexhints@latest

Install plugins
^^^^^^^^^^^^^^^
.. code-block:: yaml

   - name: Bootstrap Plex server
     id: bootstrap
     uses: LizardByte/plexhints@latest
     with:
       plugin_bundles_to_install: >-
         MyAwesomePlexPlugin.bundle
         AnotherAwesomePlexPlugin.bundle

Disable libraries
^^^^^^^^^^^^^^^^^
.. code-block:: yaml

   - name: Bootstrap Plex server
     id: bootstrap
     uses: LizardByte/plexhints@latest
     with:
       without_movies: true
       without_movies_imdb: true
       without_movies_tmdb: true
       without_shows: true
       without_music: true
       without_photos: true

Use Docker (Linux only)
^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: yaml

   - name: Bootstrap Plex server
     id: bootstrap
     uses: LizardByte/plexhints@latest
     with:
       use_docker: true

Get Outputs
^^^^^^^^^^^

.. code-block:: yaml

   - name: Another Step
     env:
       PLEXAPI_AUTH_SERVER_BASEURL: ${{ steps.bootstrap.outputs.PLEX_SERVER_BASEURL }}
       PLEXAPI_AUTH_SERVER_TOKEN: ${{ steps.bootstrap.outputs.PLEXTOKEN }}
       PLEXTOKEN: ${{ steps.bootstrap.outputs.PLEXTOKEN }}
       PLEX_APP_DATA_PATH: ${{ steps.bootstrap.outputs.PLEX_APP_DATA_PATH }}
       PLEX_PLUGIN_LOG_PATH: ${{ steps.bootstrap.outputs.PLEX_PLUGIN_LOG_PATH }}
       PLEX_PLUGIN_PATH: ${{ steps.bootstrap.outputs.PLEX_PLUGIN_PATH }}

Complete Example
^^^^^^^^^^^^^^^^

For a complete example, see our
`CI.yml <https://github.com/LizardByte/plexhints/blob/master/.github/workflows/CI.yml>`_.

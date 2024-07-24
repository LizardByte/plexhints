plexhints
=========
.. image:: https://img.shields.io/github/actions/workflow/status/lizardbyte/plexhints/CI.yml.svg?branch=master&label=CI%20build&logo=github&style=for-the-badge
   :alt: GitHub Workflow Status (CI)
   :target: https://github.com/LizardByte/plexhints/actions/workflows/CI.yml?query=branch%3Amaster

.. image:: https://img.shields.io/readthedocs/plexhints.svg?label=Docs&style=for-the-badge&logo=readthedocs
   :alt: Read the Docs
   :target: http://plexhints.readthedocs.io/

.. image:: https://img.shields.io/codecov/c/gh/LizardByte/plexhints.svg?token=1LYYVYWY9D&style=for-the-badge&logo=codecov&label=codecov
   :alt: Codecov
   :target: https://codecov.io/gh/LizardByte/plexhints

.. image:: https://img.shields.io/github/downloads/lizardbyte/plexhints/total.svg?style=for-the-badge&logo=github
   :alt: GitHub Releases
   :target: https://github.com/LizardByte/plexhints/releases/latest

.. image:: https://img.shields.io/pypi/v/plexhints.svg?style=for-the-badge&logo=pypi&label=pypi%20package
   :alt: PyPI
   :target: https://pypi.org/project/plexhints/

.. image:: https://img.shields.io/pypi/dm/plexhints?style=for-the-badge&logo=pypi&label=pypi%20downloads
   :alt: PyPI - Downloads
   :target: https://pypi.org/project/plexhints/

Overview
--------
Plexhints is a set of tools to aid in the development of plugins for Plex Media Server. It is not a framework, but
rather a set of tools that can be used to make your life easier.

Documentation is available on `Read the Docs <http://plexhints.readthedocs.io/>`__.

This project is not affiliated with Plex Inc.

Features
--------
- Python library providing type hints to aid in the development of Plex plugins. Get rid of all those IDE warnings
  and errors!
- A GitHub Action that will install and bootstrap a Plex Media Server in a CI environment. The action can install
  plugins and setup dummy libraries. Additionally the Plex token is provided as an output. This is useful for testing
  your plugin or other Plex project in a CI environment.

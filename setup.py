#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Install plexagents
"""
import setuptools

from plexagents import const

try:
    from setuptools import setup, find_namespace_packages
except ImportError:
    from setuptools import setup, find_packages
    find_namespace_packages = find_packages

# Get README.md contents
with open('README.md') as f:
    readme = f.read()

# Get requirements
requirements = []
with open('requirements.txt') as f:
    for line in f.readlines():
        if not line.startswith('#'):
            package = line.strip().split('=', 1)[0]
            requirements.append(package)

setup(
    name=const.__name__,
    version=const.__version__,
    description=const.__description__,
    author='ReenigneArcher',
    author_email='ReenigneArcher',
    url='https://github.com/PyArcher/plex_builtins',
    packages=find_namespace_packages(include=['plexagents.*']),
    install_requires=requirements,
    python_requires='==2.7',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=['plex', 'agent', 'plug-in', 'debug'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

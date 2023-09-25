#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Install plexhints
"""
import os
from pkg_resources import parse_requirements
try:
    from setuptools import setup, find_namespace_packages
except ImportError:
    from setuptools import setup, find_packages
    find_namespace_packages = find_packages

# Get version
version = {}
with open('plexhints/const.py') as handle:
    exec(handle.read(), version)

try:
    version['__version__'] += "-{}".format(os.environ['BUILD_NUMBER'])
except KeyError:
    pass

# Concatenate README files
readme_files = [
    'README.rst',
    os.path.join('docs', 'source', 'about', 'installation.rst'),
    os.path.join('docs', 'source', 'about', 'usage.rst'),
]
readme = ''
for readme_file in readme_files:
    # Get file contents
    with open(readme_file) as handle:
        readme += handle.read()
        readme += '\n'

# Get requirements
with open('requirements.txt') as handle:
    requirements = [str(req) for req in parse_requirements(handle)]

setup(
    name=version['__name__'],
    version=version['__version__'],
    description=version['__description__'],
    author='LizardByte',
    author_email='LizardByte@github.com',
    url='https://github.com/LizardByte/plexhints',
    packages=['plexhints'],
    install_requires=requirements,
    python_requires='>=2.7',
    long_description=readme,
    long_description_content_type='text/x-rst',
    keywords=['plex', 'agent', 'plug-in', 'debug'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

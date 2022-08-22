#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Install plexhints
"""
from plexhints import const

try:
    from setuptools import setup, find_namespace_packages
except ImportError:
    from setuptools import setup, find_packages
    find_namespace_packages = find_packages

# Get README.md contents
with open('README.md') as f:
    readme = f.read()

# Get requirements
with open('requirements.txt') as f:
    requirements = []
    requirement_lines = f.read().splitlines()
    for line in requirement_lines:
        if line:
            if line.startswith('#'):
                continue
            else:
                requirements.append(line)

    print(requirements)

setup(
    name=const.__name__,
    version=const.__version__,
    description=const.__description__,
    author='LizardByte',
    author_email='LizardByte',
    url='https://github.com/LizardByte/plexhints',
    packages=find_namespace_packages(include=['plexhints', 'plexhints.*']),
    install_requires=requirements,
    python_requires='>=2.7',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=['plex', 'agent', 'plug-in', 'debug'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

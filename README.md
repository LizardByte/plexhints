# plexhints

## Description
Type hinting library for Plex plugin development.

## Installation:
### Basic
```bash
python -m pip install git+https://github.com/LizardByte/plexhints.git#egg=plexhints
```

### Install to plugin modules directory
```bash
python -m pip install --target=./Contents/Libraries/Shared \
  git+https://github.com/LizardByte/plexhints.git#egg=plexhints --no-warn-script-location
```

### Use `requirements.txt` file
Filename: `./Contents/Libraries/Shared/requirements.txt`
```txt
#plexhints
git+https://github.com/LizardByte/plexhints.git#egg=plexhints

# add your other requirements here as well
```

```bash
python -m pip install --target=./Contents/Libraries/Shared \
  -r ./Contents/Libraries/Shared/requirements.txt  --no-warn-script-location
```


## Usage:
Place this at the top of your `Code/__init__.py` file. It is important to only import these when running outside
of Plex. You should only import what is necessary, but all examples are shown.

```py
# standard imports
import os
import sys

# plexhints
if 'plexscripthost' not in sys.executable.lower():  # the code is running outside of Plex
    sys.path.append(os.path.join('Contents', 'Libraries', 'Shared'))  # when running outside plex, append the path

    from plexhints import Agent, Media  # agent kit
    from plexhints import Core  # core kit
    from plexhints import CACHE_1MINUTE, CACHE_1HOUR, CACHE_1DAY, CACHE_1WEEK, CACHE_1MONTH  # constant kit
    from plexhints import Locale  # locale kit
    from plexhints import Log  # log kit
    from plexhints import HTTP  # network kit
    from plexhints import MessageContainer, MetadataItem, MetadataSearchResult, SearchResult  # object kit
    from plexhints import HTML, JSON, Plist, RSS, XML, YAML  # parse kit
    from plexhints import Prefs  # prefs kit
    from plexhints import Proxy  # proxy kit

    # extra objects
    from plexhints import BehindTheScenesObject, \
        ConcertVideoObject, \
        DeletedSceneObject, \
        FeaturetteObject, \
        InterviewObject, \
        LiveMusicVideoObject, \
        LyricMusicVideoObject, \
        MusicVideoObject, \
        OtherObject, \
        SceneOrSampleObject, \
        ShortObject, \
        TrailerObject
```

If you use submodules, you can use the same as above in your other files, except removing the `sys.path.append` method
as it is no longer needed.

```py
# standard imports
import sys

# plexhints
if 'plexscripthost' not in sys.executable.lower():  # the code is running outside of Plex
    from plexhints import Log
```

## Developer References:
A mirror of Plex's [Framework](https://github.com/squaresmile/Plex-Plug-Ins/tree/master/Framework.bundle/Contents/Resources/Versions/2/Python/Framework)

```bash
git clone https://github.com/squaresmile/Plex-Plug-Ins.git
```

A snapshot of the original Plex developer [docs](https://web.archive.org/web/https://dev.plexapp.com/docs/index.html)

## Integrate with GitHub
Filename:`.github\workflows\CI.yml`
```yaml
name: CI

on:
  pull_request:
    branches: [master, nightly]
    types: [opened, synchronize, reopened]
  push:
    branches: [master, nightly]
  workflow_dispatch:

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2
        
      - name: Install Python 2.7
        uses: actions/setup-python@v2
        with:
          python-version: '2.7'
          
      - name: Set up Python 2.7 Dependencies
        env:
          TARGET_DIR: ./Contents/Libraries/Shared
        run: |
          python -m pip --no-python-version-warning --disable-pip-version-check install --upgrade pip==20.3.4
          pip install --target=${{ env.TARGET_DIR }} -r ${{ env.TARGET_DIR }}/requirements.txt  --no-warn-script-location
          
      # This only ensure the plugin can be properly imported
      - name: Test Plex Plugin
        run: |
          python ./Contents/Code/__init__.py
          
      - name: Upload Artifacts
        uses: actions/upload-artifact@v2
        with:
          name: ${{ github.repository }}
          path: /**
```

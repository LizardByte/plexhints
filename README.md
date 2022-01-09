# plexagents

## About
- This is a library to help with testing and debugging of Plex metadata agents and plugins.
  - Essentially, the library allows you to fake the following names and constants:
    
    - Names:
      ```txt
      Agent
      Core
      HTTP
      InterviewObject
      JSON
      Locale
      Log
      MessageContainer
      MetadataSearchResult
      OtherObject
      Prefs
      Proxy
      RSS
      TrailerObject
      Util
      XML
      YAML
      ```
    - Constants:
      ```txt
      CACHE_1MINUTE
      CACHE_1HOUR
      CACHE_1DAY
      CACHE_1WEEK
      CACHE_1MONTH
      ```

## Installation:
```txt
pip install git+https://github.com/PyArcher/plexagents.git#egg=plexagents
````

## Usage:
Place this at the top of each .py file used by your metadata agent. This will only import Names that are not
already defined, which means that they will not be imported when running the agent/plugin inside of plex.
```py
from plexagents.builtins import *
```

## Integrate with github
Filename: `Contents\Libraries\Shared\requirements.txt`
```txt
#plexagent
git+https://github.com/PyArcher/plexagents.git#egg=plexagents

# add your other requirements here as well
```

Filename:`.github\workflows\create_package.yml`
```yaml
name: Create Package

on:
  pull_request:
    branches: [master, nightly]
    types: [opened, synchronize, edited, reopened]
  push:
    branches: [master, nightly, add-repo-actions]
  workflow_dispatch:

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Install Python 2.7
        uses: actions/setup-python@v2
        with:
          python-version: '2.7'
      - name: Set up Python 2.7 Dependencies
        env:
          TARGET_DIR: Contents\Libraries\Shared
        run: |
          echo "Installing Plex Agent Requirements"
          python --version
          python -m pip --no-python-version-warning --disable-pip-version-check install --upgrade pip==20.3.4
          pip install --target=${{ env.TARGET_DIR }} -r ${{ env.TARGET_DIR }}\requirements.txt  --no-warn-script-location --ignore-requires-python
      - name: Test Plex Agent
        run: |
          python --version
          python Contents\Code\__init__.py
      - name: Upload Artifacts
        if: ${{ github.event_name == 'pull_request' || github.event_name == 'workflow_dispatch' }}
        uses: actions/upload-artifact@v2
        with:
          name: ${{ github.repository }}
          path: /**
```

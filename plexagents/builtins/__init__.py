# -*- coding: utf-8 -*-
from nop import NOP


class Agent:
    """
    Fake Agent class with available subclasses.

    https://web.archive.org/web/20150113085307/http://dev.plexapp.com/docs/agents/basics.html#defining-an-agent-class
    """
    class Album:
        """This is a fake Album class."""
        pass

    class Artist:
        """This is a fake Artist class."""
        pass

    class Movies:
        """This is a fake Movies class."""
        pass

    class TV_Shows:
        """This is a fake TV_Shows class."""
        pass


def plex_test(plex_builtin, set_value=NOP()):
    """
    Try to execute the plex_builtin using exec(). If there is a NameError exception add the plex_builtin to globals().

    :param plex_builtin: str - the name to define
    :param set_value: - the value to set the name to if it's not defined, default = NOP()
    :return: True if name is defined, False if name is not defined
    """
    try:
        exec(plex_builtin)
        return True
    except NameError:
        globals()[plex_builtin] = set_value
        return False
    except Exception:
        return True


plex_globals = [
    'Core',
    'HTTP',
    'InterviewObject',
    'JSON',
    'Locale',
    'Log',
    'MessageContainer',
    'MetadataSearchResult',
    'OtherObject',
    'Prefs',
    'Proxy',
    'RSS',
    'TrailerObject',
    'Util',
    'XML',
    'YAML'
]

for name in plex_globals:
    plex_test(plex_builtin=name)

plex_constants = {
    'CACHE_1MINUTE': 60,
    'CACHE_1HOUR': 3600,
    'CACHE_1DAY': 86400,
    'CACHE_1WEEK': 604800,
    'CACHE_1MONTH': 2592000
}

for name, value in plex_constants.items():
    plex_test(plex_builtin=name, set_value=value)

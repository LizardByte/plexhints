# future imports
from __future__ import absolute_import  # import like python 3

# standard imports
import logging
import sys
import traceback

# allow writing non ascii characters to stdout
try:
    reload(sys)  # python < 3.5
except NameError:
    pass
else:
    sys.setdefaultencoding('utf-8')

# Create and Configure Logger
logging.basicConfig(stream=sys.stdout,
                    format="%(asctime)s (tbd): %(levelname)s (plexhints:tbd) - %(message)s",
                    level=logging.DEBUG)


class _LogKit:
    """
    The Log class.

    Methods
    -------
    Debug:
        Log a debug message.
    Info:
        Log a info message.
    Warn:
        Log a warning message.
    Error:
        Log an error message.
    Critical:
        Log a critical message.
    Exception:
        Log an exception message. Should only be called when handling an exception.
    Stack:
        Unknown.
    """
    def __init__(self):
        pass

    def Debug(self, fmt, *args, **kwargs):
        # type: (str, *any, **any) -> None
        """
        Log a debug message.

        Logs a message to stdout. The Plex Framework will instead log the message to the plugin's log file.

        Parameters
        ----------
        fmt : str
            The message string.
        args : any
            The values for formatting the ``fmt`` string.
        kwargs : any
            Todo.

        Examples
        --------
        >>> from plexhints.log_kit import Log
        >>> Log.Debug('This is a debug message.')
        ...
        >>> from plexhints.log_kit import Log
        >>> message_type = 'debug'
        >>> Log.Debug('This is a %s message.', message_type)
        ...
        >>> from plexhints.log_kit import Log
        >>> Log.Debug('This is a %(message_type)s message.', {'message_type': 'debug'})
        ...
        """
        logging.debug(fmt, *args, **kwargs)

    def Info(self, fmt, *args, **kwargs):
        # type: (str, *any, **any) -> None
        """
        Log a info message.

        Logs a message to stdout. The Plex Framework will instead log the message to the plugin's log file.

        Parameters
        ----------
        fmt : str
            The message string.
        args : any
            The values for formatting the ``fmt`` string.
        kwargs : any
            Todo.

        Examples
        --------
        >>> from plexhints.log_kit import Log
        >>> Log.Info('This is a info message.')
        ...
        """
        logging.info(fmt, *args, **kwargs)

    def Warn(self, fmt, *args, **kwargs):
        # type: (str, *any, **any) -> None
        """
        Log a warning message.

        Logs a message to stdout. The Plex Framework will instead log the message to the plugin's log file.

        Parameters
        ----------
        fmt : str
            The message string.
        args : any
            The values for formatting the ``fmt`` string.
        kwargs : any
            Todo.

        Examples
        --------
        >>> from plexhints.log_kit import Log
        >>> Log.Warn('This is a warning message.')
        ...
        """
        logging.warning(fmt, *args, **kwargs)

    def Error(self, fmt, *args, **kwargs):
        # type: (str, *any, **any) -> None
        """
        Log an error message.

        Logs a message to stdout. The Plex Framework will instead log the message to the plugin's log file.

        Parameters
        ----------
        fmt : str
            The message string.
        args : any
            The values for formatting the ``fmt`` string.
        kwargs : any
            Todo.

        Examples
        --------
        >>> from plexhints.log_kit import Log
        >>> Log.Error('This is an error message.')
        ...
        """
        logging.error(fmt, *args, **kwargs)

    def Critical(self, fmt, *args, **kwargs):
        # type: (str, *any, **any) -> None
        """
        Log a critical message.

        Logs a message to stdout. The Plex Framework will instead log the message to the plugin's log file.

        Parameters
        ----------
        fmt : str
            The message string.
        args : any
            The values for formatting the ``fmt`` string.
        kwargs : any
            Todo.

        Examples
        --------
        >>> from plexhints.log_kit import Log
        >>> Log.Critical('This is a critical message.')
        ...
        """
        logging.critical(fmt, *args, **kwargs)

    def Exception(self, fmt, *args, **kwargs):
        # type: (str, *any, **any) -> None
        """
        Log a info message.

        Logs a message to stdout. The Plex Framework will instead log the message to the plugin's log file.

        The same as the `Critical` method above, but appends the current stack trace to the log message.

        .. note:: This method should only be called when handling an exception.

        Parameters
        ----------
        fmt : str
            The message string.
        args : any
            The values for formatting the ``fmt`` string.
        kwargs : any
            Todo.

        Examples
        --------
        >>> from plexhints.log_kit import Log
        >>> try:
        >>>     int('Hello World!')
        >>> except ValueError:
        >>>     Log.Exception('This is an exception message.')
        ...
        Traceback (most recent call last):
        ...
        >>> from plexhints.log_kit import Log
        >>> try:
        >>>     int('Hello World!')
        >>> except ValueError as e:
        >>>     Log.Exception('Exception occurred: %s.', e)
        ...
        Traceback (most recent call last):
        ...
        """
        self.Critical(fmt, exc_info=True, *args, **kwargs)

    def Stack(self):
        """
        Log a stack message.

        Logs a message to stdout. The Plex Framework will instead log the message to the plugin's log file.

        .. Todo:: Define what the actual purpose of this is.

        Examples
        --------
        >>> from plexhints.log_kit import Log
        >>> Log.Stack()
        ...
        """
        stack = ''
        lines = traceback.format_stack()[3:-3]
        for line in lines:
            if sys.prefix not in line:
                stack += '  %s\n' % line.strip()
        self.Debug("Current stack:\n" + stack)


Log = _LogKit()

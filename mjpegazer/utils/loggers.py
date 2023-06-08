# -*- coding: utf-8 -*-

"""Logging Utitilies"""

from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path

from .constants import DEBUG, LOG_FILE, LOG_FORMAT


class Loggers:
    """
    The Loggers class manages Python logging.Logger instances
    for different components in the program.

    This class serves as a factory for Python logging.Logger instances.
    Each component in the program can obtain its own Logger instance
    by calling Loggers.get_logger() with a unique name.
    The Logger instances are configured with a common log message format
    and can optionally log messages to a file and/or in debug mode.

    Attributes
    ----------
    loggers: dict[str, logging.Logger]
        A dictionary that maps component names to their corresponding Logger instances.
    _format: str
        The format string used for log messages.
    _file: str
        The path to the file where log messages are written.
    _debug: bool
        Whether the Logger instances should operate in debug mode.

    Usage
    -----
    ```python
    from mjpegazer import get_logger
    logger = get_logger(__name__)

    def my_func(a: int, b: int):
        logger.debug("adding %s and %s", a, b)
        try:
            return a + b
        except TypeError as exception:
            logger.error("%s: can't add %s and %s", exception, repr(a), repr(b))
            raise _e from _e
    if __name__ == '__main__':
        numbers = [
            (1,1,)
            ("string", 1,)
        ]
        for a, b in numbers:
            print(
                my_func(a, b)
            )

    ```
    """

    # pylint: disable=too-few-public-methods
    loggers: dict[str, logging.Logger] = {}
    _format: str = LOG_FORMAT
    _file: str = LOG_FILE
    _debug: bool = DEBUG

    @classmethod
    def get_logger(
        cls,
        name: str,
        debug: bool = False,
    ) -> logging.Logger:
        """
        Returns a Logger instance for the specified name.

        If a Logger instance for the specified name already exists,
        the existing instance is returned.

        Otherwise, a new Logger instance is created, configured, and returned.

        The new Logger instance will log messages in debug mode if:
            the debug parameter is True or if cls._debug is True.

        Parameters
        ----------
        name : str
            The name of the component that will use the Logger instance.
        debug : bool, optional
            Whether the Logger instance should operate in debug mode.

        Returns
        -------
        logging.Logger
            The Logger instance for the specified name.
        """
        debug = debug or cls._debug
        file = cls._file
        if file:
            file = Path(file)

        logger = cls.loggers.get(name, None)
        if logger:
            return logger

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        if debug:
            logger.setLevel(logging.DEBUG)

        handlers: list[logging.Handler] = [logging.StreamHandler()]

        if file:
            handlers.append(logging.FileHandler(file))

        formatter = logging.Formatter(cls._format)
        for handler in handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        cls.loggers[name] = logger
        return logger


get_logger: Callable[..., logging.Logger] = Loggers.get_logger

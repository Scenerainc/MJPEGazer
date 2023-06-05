# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
from pathlib import Path
from collections.abc import Callable
from .constants import DEBUG, LOG_FORMAT, LOG_FILE


class Loggers:
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
        """Get a logger"""

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

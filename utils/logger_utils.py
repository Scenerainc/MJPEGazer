# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
from .constants import DEBUG, LOG_FORMAT, LOG_FILE


def get_logger(
    name: str,
    log_format: Optional[str] = None,
    file: Optional[Path | str] = None,
    debug: bool = False,
) -> logging.Logger:
    try:
        debug = debug or DEBUG
        assert debug in [True, False]
        log_format = str(log_format or LOG_FORMAT)
        file = file or LOG_FILE
        if file:
            file = Path(file)
    except (ValueError, AssertionError) as _e:
        raise ValueError("incompatible argument") from _e

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if file:
        handlers.append(logging.FileHandler(file))

    formatter = logging.Formatter(log_format)
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

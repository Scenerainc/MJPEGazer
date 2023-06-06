# -*- coding: utf-8 -*-

"""Development utilities"""

from collections.abc import Callable
from typing import Any

from .constants import DEBUG
from .exceptions import Errors
from .loggers import get_logger

logger = get_logger(__name__)


class _Trigger(Errors):
    """DEBUG Variable has not been set to True"""


def placeholder_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Placeholder function

    Does nothing, it is a placeholder for typechecked from typeguard
    in case typeguard hasn't been installed or DEBUG is not active
    """
    return func


# This doesn't yet seem to work as excepted
try:
    if not DEBUG:
        raise _Trigger
    from typeguard import typechecked
except (ModuleNotFoundError, ImportError, _Trigger) as _e:
    logger.debug("%s: not loading typechecked", _e)
    typechecked = placeholder_decorator

__all__ = ["typechecked"]

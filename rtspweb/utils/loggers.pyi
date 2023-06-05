# -*- coding: utf-8 -*-

from typing import overload
from logging import Logger

@overload
def get_logger(name: str, debug: bool = ...) -> Logger: ...

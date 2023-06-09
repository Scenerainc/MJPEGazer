# -*- coding: utf-8 -*-

from __future__ import annotations

from logging import Logger
from typing import overload

@overload
def get_logger(name: str, debug: bool = ...) -> Logger: ...

# -*- coding: utf-8 -*-

from __future__ import annotations

from os import getenv
from typing import Optional

TRUE_STRINGS: list[str] = [
    str(i).upper()
    for i in (
        "true",
        "yes",
        "y",
        "1",
    )
] 
DEBUG: bool = getenv("DEBUG", "False").upper() in TRUE_STRINGS
LOG_FORMAT: str = (
    "[%(asctime)s - %(levelname)s] %(name)s: "
    + "[%(filename)s:%(lineno)s] %(funcName)s() - %(message)s"
)
LOG_FILE: Optional[str] = getenv("LOG_FILE", None)
MIRROR_IMAGE: bool = getenv("MIRROR_IMAGE", "False").upper() in TRUE_STRINGS

FLASK_RUN_HOST: str = getenv("FLASK_RUN_HOST", "127.0.0.1")
FLASK_RUN_PORT: int = int(getenv("FLASK_RUN_PORT", "5000"))

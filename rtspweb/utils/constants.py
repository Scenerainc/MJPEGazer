# -*- coding: utf-8 -*-

"""Constants"""

from __future__ import annotations

from os import getenv
from typing import Any, Optional

TRUE_STRINGS: list[str] = [
    str(i).upper()
    for i in (
        "true",
        "yes",
        "y",
        "1",
    )
]

CV2_CAPABILITIES = int | Any  # for example cv2.CAP_FFMPEG
HEALTH_THRESHOLD: int = 42  # Q: Why is this 42?
# A: https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy
# A: In reality, it should probably be less
# A: it is the number of consecutive fails before the MJPEG object is considered 'unhealthy'

LOG_FORMAT: str = (
    "[%(asctime)s - %(levelname)s] %(name)s: "
    + "[%(filename)s:%(lineno)s] %(funcName)s() - %(message)s"
)
LOG_FILE: Optional[str] = getenv("LOG_FILE", None)
MIRROR_IMAGE: bool = getenv("MIRROR_IMAGE", "False").upper() in TRUE_STRINGS


DEBUG: bool = getenv("DEBUG", "False").upper() in TRUE_STRINGS
FLASK_RUN_HOST: str = getenv("FLASK_RUN_HOST", "127.0.0.1")
FLASK_RUN_PORT: int = int(getenv("FLASK_RUN_PORT", "5000"))
VIDEO_URL: str = getenv("VIDEO_URL", "webcam://0")

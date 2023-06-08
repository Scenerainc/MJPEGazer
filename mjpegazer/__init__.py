"""MJPEG Gazer, Capture and serve video streams over MJPEG to web browers"""

from . import core, utils
from .core import Capture, MJPEGFrames, Server
from .utils import Errors, InitializationError

__all__ = [
    "core",
    "utils",
    "Capture",
    "MJPEGFrames",
    "Server",
    "Errors",
    "InitializationError",
]

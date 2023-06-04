# -*- coding: utf-8 -*-

from __future__ import annotations

from threading import Lock
from typing import Any, Iterable, NewType, Optional

import cv2

from .constants import MIRROR_IMAGE
from .exceptions import InitializationError
from .logger_utils import get_logger

logger = get_logger(__name__)

LOCK = Lock()
CV2_CAPABILITIES = NewType("CV2_CAPABILITIES", int)  # for example cv2.CAP_FFMPEG
HEALTH_THRESHOLD = 42


class HTTPMultiPart:
    SECTION = list
    PART = bytes
    STREAM = Iterable


class Capture:
    _port: str
    _lock: Lock
    _cap: list = set([cv2.CAP_FFMPEG])

    def __init__(self, camera_port: str, lock: Optional[Lock] = None):
        self._port = camera_port
        self._lock = lock

    def __enter__(self) -> "Capture":
        if self._lock:
            self._lock.acquire()
        video_object = cv2.VideoCapture(self.camera_port, *self.capabilities)
        if not video_object.isOpened():
            raise InitializationError("Video object not available!")
        return video_object

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        ignorable_exceptions = [GeneratorExit, KeyboardInterrupt]
        if self._lock:
            self._lock.release()

        if exc_type:
            logger.warning(
                "Failed capturing frames!",
                exc_info=(exc_type, exc_val, exc_tb),
                stack_info=not issubclass(exc_type, tuple(ignorable_exceptions)),
            )
        return True

    @property
    def camera_port(self) -> str | int:
        if "webcam://" in self._port:
            return int(self._port.split("://")[-1])
        return self._port

    @property
    def capabilities(self) -> set[CV2_CAPABILITIES]:
        return self._cap


class MJPEGFrames:
    capture_object: Capture
    _failures: int = 0

    def __init__(self, capture_object: Capture):
        self.capture_object = capture_object

    @property
    def healthy(self) -> bool:
        return self._failures < HEALTH_THRESHOLD

    @property
    def _health(self):
        return self._failures

    @_health.setter
    def _health(self, value: bool) -> None:
        if value is True:
            self._failures = 0
            return None
        self._failures += 1
        if self._failures < HEALTH_THRESHOLD:
            logger.warning("Unhealthy! No frames for the last %d", self._failures)
        return None

    def __iter__(self) -> Iterable[HTTPMultiPart.PART]:
        with self.capture_object as cap:
            while cap.isOpened():
                ret, frame = cap.read()
                if ret is None:
                    self._health = False
                    logger.debug("Failed to capture frame")
                    continue
                self._health = True
                if MIRROR_IMAGE:
                    frame = cv2.flip(frame, 1)
                image = cv2.imencode(".jpg", frame)[1]
                image = image.tobytes()
                yield (
                    b"--frame\r\n"
                    + b"Content-Type: image/jpeg\r\n\r\n"
                    + image
                    + b"\r\n"
                )

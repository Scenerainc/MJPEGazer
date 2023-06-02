# -*- coding: utf-8 -*-

from __future__ import annotations
from contextlib import suppress
from threading import Lock
from typing import Iterable, Optional

import cv2

from .exceptions import InitializationError
from .constants import MIRROR_IMAGE
from .logger_utils import get_logger

logger = get_logger(__name__)

LOCK = Lock()


class VideoCapture:
    camera_port: str | int
    _lock: Lock
    _failures: int = 0
    _video_object: Optional[cv2.VideoCapture] = None

    def __init__(self, camera_port: str | int, lock: Lock = LOCK):
        if "webcam://" in camera_port:
            camera_port = int(camera_port.split("://")[-1])
        self._lock = lock
        logger.debug("Using camera %s", camera_port)
        self.camera_port = camera_port
        self.__enter__()

    def __enter__(self) -> "VideoCapture":
        if self._video_object:
            return self
        with self._lock:
            self._video_object = cv2.VideoCapture(
                self.camera_port,
                cv2.CAP_FFMPEG,
            )
            if not self._video_object.isOpened():
                raise InitializationError("Video object not available!")

    def __exit__(self, *_) -> bool:
        with self._lock:
            with suppress(AttributeError):
                self._video_object.release()
                del self._video_object
            self._video_object = None
        return False

    def restore(self) -> None:
        if not self.healthy:
            self.__exit__()
            self.__enter__()

    def activate(self) -> "VideoCapture":
        return self.__enter__()

    def close(self) -> bool:
        return self.__exit__()

    def get_frame(self) -> Optional[cv2.Mat]:
        with self._lock:
            if not self._video_object or not self.healthy:
                return None
            ret, frame = self._video_object.read()
            if not ret:
                self._failures += 1
                logger.warning(
                    "failed to capture images with %s",
                    self.camera_port,
                )
                return None
            self._failures = 0
        if MIRROR_IMAGE:
            return cv2.flip(frame, 1)
        return frame

    @property
    def healthy(self) -> bool:
        return self._failures < 42

    def __iter__(self) -> Iterable[cv2.Mat]:
        while True:
            frame = self.get_frame()
            if frame is None:
                continue
            yield frame

    @property
    def http_frames(self) -> Iterable[bytes]:
        while True:
            frame = self.get_frame()
            if frame is None:
                self.restore()
                continue
            image = cv2.imencode(".jpg", frame)[1]
            image = image.tobytes()
            yield (
                b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + image + b"\r\n"
            )

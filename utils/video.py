# -*- coding: utf-8 -*-

from __future__ import annotations
from contextlib import suppress

from typing import Iterable, Optional

import cv2

from .exceptions import InitializationError
from .constants import MIRROR_IMAGE
from .logger_utils import get_logger

logger = get_logger(__name__)


class VideoCapture:
    camera_port: str | int
    _video_object: Optional[cv2.VideoCapture] = None

    def __init__(self, camera_port: str | int = "webcam://0"):
        if "webcam" in camera_port:
            camera_port = int(camera_port.split("://")[-1])
        logger.debug("Using camera %s", camera_port)
        self.camera_port = camera_port

    def __enter__(self) -> "VideoCapture":
        if self._video_object:
            return self

        self._video_object = cv2.VideoCapture(self.camera_port)
        if not self._video_object.isOpened():
            raise InitializationError("Video object not available!")
        return self

    def __exit__(self, *args) -> bool:
        with suppress(AttributeError):
            self._video_object.release()
        self._video_object = None
        return None in args

    def activate(self) -> 'VideoCapture':
        return self.__enter__()

    def close(self) -> bool:
        return self.__exit__()

    @property
    def frames(self) -> Iterable[bytes]:
        if not self._video_object:
            raise IndentationError("Please Launch VideoCapture first! i.e. video_capture_instance.activate()")
        while True:
            ret, frame = self._video_object.read()
            if not ret:
                logger.error(
                    "failed to capture images with %r: $r", self._video_object, image
                )
                break
            if MIRROR_IMAGE:
                frame = cv2.flip(frame, 1)
            image = cv2.imencode(".jpg", frame)[1]
            yield image.tobytes()

    @property
    def http_frames(self) -> Iterable[bytes]:
        for image in self.frames:
            yield (b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + image + b"\r\n")

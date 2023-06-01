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

    def __init__(self, camera_port: str | int):
        if "webcam://" in camera_port:
            camera_port = int(camera_port.split("://")[-1])
        logger.debug("Using camera %s", camera_port)
        self.camera_port = camera_port

    def __enter__(self) -> "VideoCapture":
        if self._video_object:
            ret, frame = self._video_object.read()
            if ret:
                return self

        self.__exit__()
        self._video_object = cv2.VideoCapture(self.camera_port)
        if not self._video_object.isOpened():
            raise InitializationError("Video object not available!")
        return self

    def __exit__(self, *args) -> bool:
        with suppress(AttributeError):
            self._video_object.release()
        self._video_object = None
        return None in args

    def activate(self) -> "VideoCapture":
        return self.__enter__()

    def close(self) -> bool:
        return self.__exit__()

    def get_frame(self) -> Optional[cv2.Mat]:
        if not self._video_object:
            raise InitializationError("Please launch the instance instance.launch()")
        ret, frame = self._video_object.read()
        if not ret:
            logger.warning(
                "failed to capture images with %s: %s",
                self._video_object,
                self.camera_port,
            )
            return None
        if MIRROR_IMAGE:
            return cv2.flip(frame, 1)
        return frame

    def __iter__(self) -> Iterable[cv2.Mat]:
        if not self._video_object:
            raise InitializationError(
                'Invalid Usage, example:\n\twith VideoCapture() as frame_server:\n\t\tfor image in frame_server:\n\t\t\tprint(f"received an image with type {type(i)}")'
            )
        while self._video_object.isOpened():
            frame = self.get_frame()
            if not frame:
                continue
            yield frame

    @property
    def http_frames(self) -> Iterable[bytes]:
        self.activate()
        while self._video_object.isOpened():
            frame = self.get_frame()
            if frame is None:
                continue
            image = cv2.imencode(".jpg", frame)[1]
            image = image.tobytes()
            yield (
                b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + image + b"\r\n"
            )

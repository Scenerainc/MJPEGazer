# -*- coding: utf-8 -*-

from __future__ import annotations

from contextlib import AbstractContextManager, suppress
from threading import Lock
from types import TracebackType
from typing import Optional, Tuple, Union, overload

import cv2
from numpy import generic, ndarray

from rtspweb.utils import InitializationError, get_logger, typechecked
from rtspweb.utils.constants import CV2_CAPABILITIES

logger = get_logger(__name__)

EXC_INFO = Tuple[BaseException | None, BaseException | None, TracebackType | None]


@overload
class VideoCapture:
    """
    This is just here to satisfy syntax highlighter

    The actual used class is cv2.VideoCapture
    """

    def isOpened() -> bool:
        ...

    def read() -> Tuple[bool, ndarray[int, generic]]:
        ...


@typechecked
class Capture(AbstractContextManager):
    _port: str
    lock: Lock
    capabilities: set[CV2_CAPABILITIES] = set([cv2.CAP_FFMPEG])
    _capture: VideoCapture | cv2.VideoCapture | None = None

    def __init__(self, camera_port: str, lock: Optional[Lock] = None):
        """
        Initialize a Capture object.

        Parameters
        ----------
        camera_port : str
            The port to the camera.
        lock : Optional[Lock]
            Optional lock to ensure thread-safety.
        """
        self._port = camera_port
        self._lock = lock

    def __enter__(self) -> Union[VideoCapture, cv2.VideoCapture]:
        """
        Context manager entry method.

        Returns
        -------
        Capture
            A Capture object.

        Raises
        ------
        InitializationError
            If the video object is not available.
        """
        if self._lock:
            self._lock.acquire()
        self._capture = cv2.VideoCapture(self.camera_port, *self.capabilities)
        if not self._capture.isOpened():
            raise InitializationError("Video object not available!")
        return self._capture

    def __exit__(
        self,
        exc_type: Optional[BaseException],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """
        Context manager exit method.

        Parameters
        ----------
        exc_type
            Exception type.
        exc_val
            Exception value.
        exc_tb
            Exception traceback.

        Returns
        -------
        bool
            Always True, indicating exceptions should be suppressed.
        """
        exc_info = (exc_type, exc_val, exc_tb)
        with suppress(AttributeError):
            self._capture.release()
            self._capture = None
        if self._lock:
            self._lock.release()
        if None not in exc_info:
            logger.warning(
                "Failed capturing frames!",
                exc_info=exc_info,
            )
        return True

    @property
    def camera_port(self) -> str | int:
        """
        Get the camera port.

        Returns
        -------
        Union[str, int]
            Camera port as a string or an integer.
        """
        if "webcam://" in self._port:
            return int(self._port.split("://")[-1])
        return self._port

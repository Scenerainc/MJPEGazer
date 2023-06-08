# -*- coding: utf-8 -*-

"""cv2 Video Capture wrapper"""

from __future__ import annotations

from contextlib import AbstractContextManager, suppress
from threading import Lock
from types import TracebackType
from typing import Optional, Tuple, Union, overload

import cv2
from numpy import generic, ndarray

from mjpegazer.utils import InitializationError, get_logger, typechecked
from mjpegazer.utils.constants import CV2_CAPABILITIES

logger = get_logger(__name__)


@overload
class VideoCapture:
    """
    This is just here to satisfy syntax highlighter

    The actual used class is cv2.VideoCapture

    NOTE this 'stub' can soon be removed
    NOTE (OpenCV 5 seems to plan on including type stubs *fingers crossed*)
    """

    # pylint: disable=invalid-name
    # pylint: disable=missing-function-docstring

    def isOpened(self) -> bool:
        ...

    def read(self) -> Tuple[bool, ndarray[int, generic]]:
        ...


@typechecked
class Capture(AbstractContextManager):
    """Capture class is a context manager for safely handling video capturing operations.

    It allows the capture of video data from a camera port with optional thread-safety.
    The context manager makes sure that the resources are properly cleaned up after use.

    The `camera_port` is used to specify the source of the video capturing,
    and could be either a path to a video file or an integer specifying
    the index of a webcam.

    Parameters
    ----------
    AbstractContextManager : class
        The base class which provides a mechanism to safely handle resources.

    Returns
    -------
    Union[VideoCapture, cv2.VideoCapture]
        A VideoCapture object.

    Raises
    ------
    InitializationError
        When the video source is not available or not properly initialized.

    Usage:
    ```python
    with Capture("my video url") as cap:
        while cap.isOpened():
            ret, frame = cap.read()
            ...
    """

    # pylint: disable=no-member
    # NOTE the pylint no member can soon be removed
    # NOTE (OpenCV 5 seems to plan on including type stubs *fingers crossed*)
    _port: str
    lock: Lock
    capabilities: set[CV2_CAPABILITIES] = set([cv2.CAP_FFMPEG])
    _capture: Union[VideoCapture, cv2.VideoCapture, None] = None

    def __init__(self, camera_port: str, lock: Optional[Lock] = None):
        """Initialize a Capture object.

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
        """Context manager entry method.

        Returns
        -------
        CaptureObject
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
        """Context manager exit method.

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
    def camera_port(self) -> Union[str, int]:
        """Get the camera port.

        Returns
        -------
        Union[str, int]
            Camera port as a string or an integer.
        """
        if "webcam://" in self._port:
            return int(self._port.split("://")[-1])
        return self._port

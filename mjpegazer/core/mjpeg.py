# -*- coding: utf-8 -*-

"""Motion JPEG frame generation"""

from contextlib import AbstractContextManager
from typing import ByteString, Iterable, Union

import cv2
from numpy import generic, ndarray

from mjpegazer.utils import get_logger, typechecked
from mjpegazer.utils.constants import HEALTH_THRESHOLD, MIRROR_IMAGE

from .capture import Capture

logger = get_logger(__name__)


@typechecked
class MJPEGFrames:
    """MJPEG http multipart 'parts'

    MJPEG, or Motion JPEG, is a video compression format where
    each video frame is separately compressed as a JPEG image.
    It's straightforward to use and widely supported,
    but less efficient than more modern codecs.

    Multipart headers are part of the
        MIME (Multipurpose Internet Mail Extensions) standard,
    used for transferring different types of data over the internet.
    They allow a single HTTP response to contain multiple different data parts,
    each with its own headers and content.

    In the context of MJPEG,
    multipart headers are often used in live streaming scenarios.
    A common technique is to stream an MJPEG video over HTTP
        using "multipart/x-mixed-replace" content-type.

    Each frame is sent as a separate part of the response,
    separated by boundaries defined in the multipart header.
    This allows the video to be streamed continuously,
    with the client replacing each part (i.e., frame) as it arrives.

    Properties
    ----------
    healthy : bool
        Video Capturerer Health


    Yields
    ------
    ByteString
        image bytes in a http 'frame'

    Example
    -------
    ```python
    import cv2
    from flask import Flask, Reponse
    from contextlib import AbstractContextManager
    from mjpegazer.core.capture import Capture
    from mjpegazer.core.mjpeg import MJPEGFrames


    app = Flask(__name__)


    @app.route("/live")
    def live() -> Response:
        video_stream = Capture("my video url")
        mjpeg_frames = MJPEGFrames(video_stream)
        return Response(
            mjpeg_frames,
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    if __name__ == '__main__':
        app.run(host="127.0.0.1", port=5000)

    ```

    """

    capture_object: Union[Capture, AbstractContextManager]
    _failures: int = 0

    def __init__(self, capture_object: Union[Capture, AbstractContextManager]):
        """
        Initialize an MJPEGFrames object.

        Parameters
        ----------
        capture_object : Capture
            A Capture object.
        """
        self.capture_object = capture_object

    def __iter__(self) -> Iterable[ByteString]:
        """
        Return an iterator for the MJPEGFrames object.

        Returns
        -------
        Iterable[ByteString]
            JPEG image bytes packaged as parts of an HTTP MJPEG multipart stream.
        """
        ## ------------------- NOTE ---------- ##
        ## For the typechecking, linting, etc  ##
        frame: ndarray[int, generic]
        jpeg: ndarray[int, generic]
        # pylint: disable=no-member
        ## ----------------------------------- ##

        with self.capture_object as cap:  # get the cv2.VideoCapture object from the context manager
            while cap.isOpened():
                try:
                    ret, frame = cap.read()
                    if ret is None:  # check if there is a frame in the buffer
                        self._failures += 1  # Report failure to the health check
                        logger.debug("Failed to capture frame")
                        continue  # finish this loop
                    self._failures = 0  # Reset health counter
                    if MIRROR_IMAGE:
                        frame = cv2.flip(frame, 1)
                    jpeg = cv2.imencode(".jpg", frame)[1]
                    yield (  # Yield payload with '--frame' boundry in header
                        b"--frame\r\n"
                        + b"Content-Type: image/jpeg\r\n\r\n"
                        + jpeg.tobytes()
                        + b"\r\n"
                    )
                except GeneratorExit:
                    break  # graceful exit

    @property
    def healthy(self) -> bool:
        """
        Check if the MJPEGFrames object is healthy.

        Returns
        -------
        bool
            True if the object is healthy, False otherwise.
        """
        return self._failures < HEALTH_THRESHOLD

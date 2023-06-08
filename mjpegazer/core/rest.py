# -*- coding: utf-8 -*-

"""Flask"""

from __future__ import annotations

from threading import Lock

from flask import Flask, Response

from mjpegazer.utils import get_logger, typechecked

from .capture import Capture
from .mjpeg import MJPEGFrames

LOCK = Lock()

logger = get_logger(__name__)


@typechecked
class Server:
    """
    The Server class is a Flask server that can be configured to stream MJPEG video.

    This class serves a Flask server that streams MJPEG video frames over HTTP.
    It also exposes a health check endpoint that returns the status of the video stream.

    Attributes
    ----------
    MJPEG: MJPEGFrames
        A MJPEGFrames object which generates the MJPEG video frames to be streamed by the server.

    Usage
    -----
    >>> Server.configure("my video url")
    >>> app = Server.flask(__name__)
    >>> app.run(...)

    """

    MJPEG: MJPEGFrames

    @classmethod
    def configure(cls, video_url: str, lock: Lock = LOCK) -> None:
        """
        Configures the Server class by initializing a MJPEGFrames object.

        Parameters
        ----------
        video_url : str
            The URL of the video source to stream.
        lock : Lock
            A threading.Lock object to ensure thread safety.
            Default LOCK is used if not provided,
            Can be set to `None`.
        """
        capture_object = Capture(video_url, lock)
        cls.MJPEG = MJPEGFrames(capture_object)

    @classmethod
    def live(cls) -> Response:
        """
        Returns a Flask Response object that streams the MJPEG video frames.

        Returns
        -------
        Response
            A Flask Response object with the MJPEG video frames as the response data.

        Notes
        -----
        The application could probably serve more 'users':
            If a MJPEGFrames object is created per request to this function.

            However, it is also out of scope for this example
            and as it is MJPEG a Gigabit link can only serve to so many anyway.

            Though this in turn could be 'negated' by lowering the image qualitity
        """
        try:
            return Response(
                cls.MJPEG,
                mimetype="multipart/x-mixed-replace; boundary=frame",
            )
        except Exception as _e:
            logger.exception(_e)
            raise _e from _e

    @classmethod
    def health(cls) -> Response:
        """
        Returns a Flask Response object that indicates the health status of the video stream.

        Returns
        -------
        Response
            A Flask Response object with the health status ("True" or "False") as the response data.
            The HTTP status code is 200 if the video stream is healthy, otherwise it's 503.
        """
        try:
            if cls.MJPEG.healthy:
                return Response("True", status=200)
            return Response("False", status=503)
        except Exception as _e:
            logger.exception(_e)
            raise _e from _e

    @classmethod
    def flask(
        cls,
        name: str,
        live_route: str = "/live",
        health_route: str = "/health",
    ) -> Flask:
        """
        Returns a Flask application that is ready to serve the video stream.

        Parameters
        ----------
        name : str
            The name to use for the Flask application.

        Returns
        -------
        Flask
            A Flask application with the '/live' and '/health' endpoints configured.
        """
        app = Flask(name)
        app.add_url_rule(live_route, view_func=cls.live)
        app.add_url_rule(health_route, view_func=cls.health)
        return app

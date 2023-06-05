# -*- coding: utf-8 -*-

from __future__ import annotations

from threading import Lock

from flask import Flask, Response

from rtspweb.utils import get_logger, typechecked
from .capture import Capture
from .mjpeg import MJPEGFrames


LOCK = Lock()

logger = get_logger(__name__)


@typechecked
class Server:
    MJPEG: MJPEGFrames

    @classmethod
    def configure(cls, video_url: str, lock: Lock = LOCK):
        capture_object = Capture(video_url, lock)
        cls.MJPEG = MJPEGFrames(capture_object)

    @classmethod
    def live(cls) -> Response:
        return Response(
            cls.MJPEG,
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    @classmethod
    def health(self) -> Response:
        if self.MJPEG.healthy:
            return Response("True", status=200)
        return Response("False", status=503)

    @classmethod
    def flask(cls, name) -> Flask:
        app = Flask(name)
        app.add_url_rule("/live", view_func=cls.live)
        app.add_url_rule("/health", view_func=cls.health)
        return app

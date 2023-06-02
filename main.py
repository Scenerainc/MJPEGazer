# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from __future__ import annotations

from flask import Flask, Response

from utils import (
    get_logger,
    DEBUG,
    VideoCapture,
    FLASK_RUN_PORT,
    FLASK_RUN_HOST,
    VIDEO_URL,
)

app = Flask(__name__)
logger = get_logger(__name__)
frame_server = VideoCapture(camera_port=VIDEO_URL)


@app.route("/live")
def live() -> Response:
    """Caveats:

    OpenCV fails reading frames,
    cv2.VideoCapture object has to be recreated to resolve.

    This is done by calling `FRAME_SERVER.activate()` again, i.e. reload the page
    """
    try:
        return Response(
            frame_server.http_frames,
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )
    except Exception as _e:
        logger.exception(_e)
        frame_server.restore()


@app.route("/health")
def health() -> Response:
    if frame_server.healthy:
        return Response("True", status=200)
    return Response("False", status=503)


if __name__ == "__init__":
    frame_server.activate()

if __name__ == "__main__":
    try:
        frame_server.activate()
        app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        pass
    except Exception as _e:
        logger.exception(_e)
    frame_server.close()
    logger.info("Exit")

# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from __future__ import annotations

from threading import Lock

from flask import Flask, Response

from utils import DEBUG, FLASK_RUN_HOST, FLASK_RUN_PORT, VIDEO_URL, get_logger
from utils.video import Capture, MJPEGFrames

LOCK = Lock()
app = Flask(__name__)
logger = get_logger(__name__)
# frame_server = VideoCapture(camera_port=VIDEO_URL)

capture_object = Capture(camera_port=VIDEO_URL, lock=LOCK)
MJPEG = MJPEGFrames(capture_object)
 

@app.route("/live")
def live() -> Response:
    """Caveats:

    OpenCV fails reading frames,
    cv2.VideoCapture object has to be recreated to resolve.

    This is done by calling `FRAME_SERVER.activate()` again, i.e. reload the page
    """
    return Response(
        MJPEG,
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/health")
def health() -> Response:
    if MJPEG.healthy:
        return Response("True", status=200)
    return Response("False", status=503)


if __name__ == "__main__":
    try:
        app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        pass
    except Exception as _e:
        logger.exception(_e)
    logger.info("Exit")

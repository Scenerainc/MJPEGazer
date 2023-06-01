# -*- coding: utf-8 -*-
#!/usr/bin/env python

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

logger = get_logger(__name__)

FRAME_SERVER = VideoCapture(camera_port=VIDEO_URL)
FRAME_SERVER.activate()

app = Flask(__name__)


@app.route("/live")
def live() -> Response:
    """Caveats:

    OpenCV fails reading frames,
    cv2.VideoCapture object has to be recreated to resolve.

    This is done by calling `FRAME_SERVER.activate()` again, i.e. reload the page
    """
    return Response(
        FRAME_SERVER.http_frames, mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    try:
        FRAME_SERVER.activate()
        app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        pass
    except Exception as _e:
        logger.exception(_e)
    FRAME_SERVER.close()
    logger.info("Exit")

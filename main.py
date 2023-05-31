# -*- coding: utf-8 -*-
#!/usr/bin/env python

from __future__ import annotations

from flask import Flask, Response

from utils import get_logger, DEBUG, VideoCapture, FLASK_RUN_PORT, FLASK_RUN_HOST

logger = get_logger(__name__)

app = Flask(__name__)
FRAME_SERVER = VideoCapture(camera_port="webcam://0")


@app.route("/live")
def live() -> Response:
    FRAME_SERVER.activate()
    return Response(
        FRAME_SERVER.http_frames, mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    endpoint = dict(
        host=FLASK_RUN_HOST,
        port=FLASK_RUN_PORT
    )

    try:
        FRAME_SERVER.activate()
        app.run(**endpoint, debug=DEBUG)
    except KeyboardInterrupt:
        pass
    except Exception as _e:
        logger.exception(_e)
    FRAME_SERVER.close()
    logger.info("Exit")

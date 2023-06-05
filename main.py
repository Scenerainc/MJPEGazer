# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from rtspweb.core import Server
from rtspweb.utils import get_logger
from rtspweb.utils.constants import VIDEO_URL, FLASK_RUN_HOST, FLASK_RUN_PORT, DEBUG

logger = get_logger(__name__)


Server.configure(VIDEO_URL)
app = Server.flask(__name__)

if __name__ == "__main__":
    try:
        app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        pass
    except Exception as _e:
        logger.exception(_e)
    logger.info("Exit")

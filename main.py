# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""Application Entrypoint"""

from mjpegazer import Server
from mjpegazer.utils import get_logger, constants


logger = get_logger(__name__)


Server.configure(constants.VIDEO_URL)
app = Server.flask(__name__)

if __name__ == "__main__":
    try:
        app.run(
            host=constants.FLASK_RUN_HOST,
            port=constants.FLASK_RUN_PORT,
            debug=constants.DEBUG,
        )
    except KeyboardInterrupt:
        pass
    logger.info("Exit")

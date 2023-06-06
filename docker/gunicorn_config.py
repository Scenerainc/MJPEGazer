"""Gunicorn settings"""

from os import getenv

host = getenv("FLASK_RUN_HOST", "0.0.0.0")
port = getenv("FLASK_RUN_PORT", "5000")

bind = f"{host}:{port}"

# pylint: disable=invalid-name
workers = 2
threads = 2
timeout = 5
preload_app = True
# pylint: enable=invalid-name

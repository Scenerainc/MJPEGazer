from os import getenv

host = getenv("FLASK_RUN_HOST", "0.0.0.0")
port = getenv("FLASK_RUN_PORT", "5000")

bind = f"{host}:{port}"

workers = 8
threads = 8
timeout = 10
# preload_app = True

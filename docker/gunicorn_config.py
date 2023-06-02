from os import getenv

host = getenv("FLASK_RUN_HOST", "0.0.0.0")
port = getenv("FLASK_RUN_PORT", "5000")

bind = f"{host}:{port}"

workers = 2
threads = 3
timeout = 10
# preload_app = True

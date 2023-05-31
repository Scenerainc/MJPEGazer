# Title

## Getting started:

> Optional
>
> ```sh
> python3 -m venv .venv
> ```

```sh
python3 -m pip install -r requirements.txt
```

```sh
VIDEO_URL="webcam://0" python3 main.py
```

> alternatively
>
> ```sh
> export "FLASK_APP=main.py"
> export "VIDEO_URL=http://webcam.rhein-taunus-krematorium.de/mjpg/video.mjpg"
>
> python3 -m flask run
> ```

### Docker

```bash
export DOCKER_BUILDKIT=1
docker build -t rtspweb:local --file=docker/Dockerfile .

docker run --rm -it -p 127.0.0.1:5000:5000 -e "VIDEO_URL=http://webcam.rhein-taunus-krematorium.de/mjpg/video.mjpg" rtspweb:local
```

## Environment Variables

- `DEBUG`: Run with debug messages (set to `True` | `yes` | `y` | `1` *case insensitive* to activate. default = `False`)
- `LOG_FILE`: File to log to (default = `None`)
- `MIRROR_IMAGE`: Mirror image output (set to `True` | `yes` | `y` | `1` *case insensitive* to activate. default = `False`)

- `FLASK_RUN_HOST`: Flask web server host (default = `127.0.0.1`)
- `FLASK_RUN_PORT`: Flask web server port, (default = `5000`)
- `VIDEO_URL`: URL to video (default = `webcam://0`)

# MJPEGazer

This is an OpenCV HTTP mjpeg server, among others, suitable for viewing RTSP streams in a [(supported)](https://en.wikipedia.org/wiki/Motion_JPEG#Applications) browser.

## License

Please see the [LICENSE file](./LICENSE)

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

You'll have to enable BuildKit to build the container

```sh
export DOCKER_BUILDKIT=1
```

Build

```sh
docker compose build
```

Run

```sh
docker compose up -d
```

> Alternatively, with the docker cli
>
> Build
>
> ```sh
> docker build                                  \
>     -t localhost.local/mjpegazer:local        \
>     --file=docker/Dockerfile                  \
>     ${GIT_ROOT:-.}
> ```
>
> Run
>
> ```sh
> docker run --rm -it -p 127.0.0.1:5000:5000                                    \
>     -e "VIDEO_URL=http://webcam.rhein-taunus-krematorium.de/mjpg/video.mjpg"  \
>     --name MJPEGazer                                                          \
>     localhost.local/mjpegazer:local                                    
> ```

## Environment Variables

- `DEBUG`: Run with debug messages (set to `True` | `yes` | `y` | `1` *case insensitive* to activate. default = `False`)
- `LOG_FILE`: File to log to (default = `None`)
- `MIRROR_IMAGE`: Mirror image output (set to `True` | `yes` | `y` | `1` *case insensitive* to activate. default = `False`)
- `FLASK_RUN_HOST`: Flask web server host (default = `127.0.0.1`)
- `FLASK_RUN_PORT`: Flask web server port, (default = `5000`)
- `VIDEO_URL`: URL to video (default = `webcam://0`)

## Development

Please see the file [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)


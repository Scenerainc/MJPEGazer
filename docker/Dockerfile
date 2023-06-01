FROM ubuntu AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG="C.UTF-8"

RUN apt-get update && apt-get install -y            \
    curl   python3      python3-pip	python3-venv    \
    python3-opencv      ffmpeg	         	        \
    libopencv-highgui-dev    		libavcodec-dev	\
    libopencv-contrib-dev
# Potential TODO, find out which of these packages
# are not required at runtime and move them to the builder stage

FROM base as builder

COPY requirements.txt .

RUN apt-get update && apt-get install -y            \
    gcc cpp cmake                                && \
    python3 -m pip install -U 				        \
    pip wheel setuptools cmake cython 	         && \
    mkdir -p /tmp/wheels                         && \
    python3 -m  pip wheel				            \
    --no-binary=python-opencv-headless		        \
    --wheel-dir=/tmp/wheels   			            \
    -r requirements.txt gunicorn

RUN python3 -m venv /venv       			     && \
    /venv/bin/python -m pip install 		        \
    --find-links=/tmp/wheels --no-cache 			\
    --prefer-binary -U -r requirements.txt gunicorn

FROM base AS runtime

COPY --from=builder --chown=0:0 --chmod=755         \
    /venv                       /venv

COPY --chown=0:0    --chmod=555                     \
    .                           /app

COPY --chown=0:0    --chmod=755                     \
    docker/gunicorn_config.py   /venv


ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

FROM runtime

HEALTHCHECK CMD curl -fs http://localhost:${FLASK_RUN_PORT}/health || exit 1

WORKDIR /app
USER 1010:1010

#CMD ["/venv/bin/python3", "-m", "flask", "run"]

ENTRYPOINT [ "/venv/bin/python3", "-m", "gunicorn", "--config=/venv/gunicorn_config.py" ]
CMD ["main:app" ]

FROM ubuntu AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG="C.UTF-8"

RUN apt-get update && apt-get install -y                \
    python3            python3-pip	python3-opencv  \
    libopencv-highgui-dev    libopencv-contrib-dev	\
    ffmpeg             libavcodec-dev

FROM base as wheels

COPY requirements.txt ./

RUN apt-get update && apt-get install -y                \
	gcc cpp cmake                                && \
    python3 -m pip install -U 				\
	pip wheel setuptools cmake cython 	     && \
    mkdir -p /local/wheels                           && \
    python3 -m  pip wheel				\
	--no-binary=python-opencv-headless		\
	--wheel-dir=/local/wheels   			\
	-r requirements.txt                          && \
    chmod +rx -R /local/wheels

FROM base AS runtime

COPY --chmod=755 . /app

RUN --mount=type=bind,target=/wheels,source=/local/wheels,from=wheels	\
    python3 -m pip install --find-links=/wheels --no-cache        \
    --no-cache --prefer-binary -U -r /app/requirements.txt

FROM runtime
WORKDIR /app

#ENV DEBUG=True
#ENV FLASK_DEBUG=True
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["python3", "-m", "flask", "run"]

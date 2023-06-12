FROM ubuntu AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG="C.UTF-8"

RUN apt-get update && apt-get install -y        \
    --no-install-recommends                     \
    curl                                        \
    python3                                  && \
    rm -rf /var/lib/apt/lists/*

FROM base AS builder

COPY requirements.txt .

RUN apt-get update && apt-get install -y        \
    python3-pip                                 \
    python3-venv                             && \
    rm -rf /var/lib/apt/lists/*              && \
    python3 -m venv /venv                    && \
    /venv/bin/python -m pip install             \
    --no-cache --prefer-binary -U               \
    -r requirements.txt gunicorn

FROM base AS runtime

COPY --chown=0:0    --chmod=555                 \
    .                           /app
# Owner: 0:0 (aka: ROOT:ROOT), Permissions (Owner, Group, Other): r-x, r-x, r-x

COPY --from=builder --chown=0:0 --chmod=755     \
    /venv                       /venv
# Owner: 0:0 (aka: ROOT:ROOT), Permissions (Owner, Group, Other): rwx, r-x, r-x
# Could be changed to r-x, r-x, r-x (--chmod=555)
# but this will not allow you to make changes to the file if mounted as a volume

COPY --chown=0:0    --chmod=755                 \
    docker/gunicorn_config.py   /venv
# Owner: 0:0 (aka: ROOT:ROOT), Permissions (Owner, Group, Other): rwx, r-x, r-x
# Could be changed to r-x, r-x, r-x (--chmod=555)

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

FROM runtime

ARG GIT_COMMIT=unspecified
LABEL GIT_COMMIT=$GIT_COMMIT

HEALTHCHECK                                     \
    --start-period=10s                          \
    --interval=5s                               \
    --retries=3                                 \
    CMD curl --fail --silent                    \ 
    http://localhost:${FLASK_RUN_PORT}/health || exit 1

WORKDIR /app
USER 1010:1010

#CMD ["/venv/bin/python3", "-m", "flask", "run"]

ENTRYPOINT [ "/venv/bin/python3", "-m", "gunicorn", "--config=/venv/gunicorn_config.py" ]
CMD ["main:app" ]

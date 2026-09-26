# syntax=docker/dockerfile:1

# --- build: dependencies into /venv ------------------------------------------
# uwsgi has no wheels, so it is compiled here and only the venv is carried over
FROM python:3.12-slim AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libc6-dev \
 && rm -rf /var/lib/apt/lists/*
RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH
WORKDIR /src
COPY setup.py setup.cfg ./
COPY vinnyexpres vinnyexpres
RUN pip install --no-cache-dir .

# --- serve: uwsgi speaking plain HTTP on :8080 as an unprivileged user -------
FROM python:3.12-slim
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app
COPY --from=build /venv /venv
WORKDIR /app
COPY config.py uwsgi.ini ./
COPY vinnyexpres vinnyexpres
COPY templates templates
COPY assets assets
# /app first on the path: the app finds templates/ and assets/ relative to its package
# directory, and config.py is a top-level module that isn't part of the installed package
ENV PATH=/venv/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
USER 10001
EXPOSE 8080
# die-on-term: stop on SIGTERM (uwsgi would otherwise reload), so pods shut down cleanly
CMD ["uwsgi", "--http-socket", "0.0.0.0:8080", "--die-on-term", "uwsgi.ini"]

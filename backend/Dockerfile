# Production controller image: application code is baked in (not bind
# mounted), so the image is self-contained and reproducible. Only
# backend/config/ is expected to be supplied via a volume at run time — it
# holds secrets, the encrypted SQLite store and HomeKit pairing state, none
# of which belong in an image layer. Rebuild (docker compose up --build) to
# pick up code changes; config changes take effect on container restart.
FROM python:3.11-slim

# No apt packages needed: pyusb/nfcpy import fine without the libusb shared
# library present (it's only dlopen'd if something actually opens a USB
# device, which this controller's WebSocket bridge flow never does). Keeping
# this image apt-free also sidesteps docker-clean/dpkg failures seen under
# some restricted container runtimes (e.g. memory-constrained hosts).

COPY requirements.txt /tmp/requirements.txt
# PIP_PROGRESS_BAR=off (env, not just a CLI flag): modern pip's default
# progress bar spawns a background render thread, which fails with "can't
# start new thread" under container runtimes with a low pids/thread limit
# (seen alongside low memory limits on some constrained hosts). A CLI flag
# on the outer pip call does not propagate to the subprocess pip that pip
# spawns internally for isolated source builds; the env var does.
ENV PIP_PROGRESS_BAR=off
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Runs as an unprivileged user rather than the image default (root). UID/GID
# are pinned (rather than left to useradd's next-free-system-UID default) so
# `chown` on the host-side config/ bind mount (see README) targets a stable,
# known value across rebuilds instead of whatever happened to be free.
RUN groupadd --system --gid 1000 controller \
    && useradd --system --uid 1000 --gid 1000 --create-home \
       --home-dir /app --shell /usr/sbin/nologin controller

WORKDIR /app
COPY --chown=controller:controller . .
RUN mkdir -p /app/config && chown controller:controller /app/config

USER controller
ENV PYTHONPATH=/app
ENTRYPOINT ["python", "run_controller.py"]

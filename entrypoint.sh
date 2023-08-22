#!/bin/sh
set -euo pipefail

cleanup () {
    kill -s SIGTERM $!
    exit 0
}

trap cleanup SIGINT SIGTERM

exec python3 -u /app/main.py $@


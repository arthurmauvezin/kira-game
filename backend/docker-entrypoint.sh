#!/bin/sh

set -euo pipefail

exec su-exec python:python "$@"

#!/bin/sh
set -e

if [ "$ENV" = "LOCAL" ] || [ "$ENV" = "TEST" ]; then
  echo "Starting server in local env"
  exec uvicorn app:app --reload --host 0.0.0.0 --port 8000
else
  echo "Starting server in production env"
  exec uvicorn app:app --host 0.0.0.0 --port 8000
fi
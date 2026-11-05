#!/bin/bash

# Load and export variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi


# curl "localhost:8000/api/redis/read" \
#   -H "Content-Type: application/json" 

# curl "${CUSTOM_DOMAIN}/api/redis/read-wo-password" \
#   -H "Content-Type: application/json" \
#   -H "x-edge-api-key: ${EDGE_API_KEY_1}"

# curl "${CUSTOM_DOMAIN}/api/redis/read" \
#   -H "Content-Type: application/json" \
#   -H "x-edge-api-key: ${EDGE_API_KEY_1}"

curl "${CUSTOM_DOMAIN}/api/headers" \
  -H "Content-Type: application/json" \
  -H "x-edge-api-key: ${EDGE_API_KEY_1}"
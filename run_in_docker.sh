#!/bin/bash -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Build docker
# The name of the docker, must be in lowercase
DOCKER_IMAGE=lynx_datafetcher_docker
docker build . -f Dockerfile -t ${DOCKER_IMAGE}
docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE}

# Run in docker
CMD="python3 src/main.py"
#TODO use .env for API_KEY
docker run -it -v ${PROJECT_DIR}:/usr/src/app ${DOCKER_IMAGE}:latest ${CMD}
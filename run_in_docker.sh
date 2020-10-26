#!/bin/bash -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Build docker
# The name of the docker, must be in lowercase
DOCKER_IMAGE=lynx_datafetcher_docker
docker build . -f Dockerfile -t ${DOCKER_IMAGE}
docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE}

# Run in docker
DOCKER_DIR="/usr/src/app"
CMD="python3 src/main.py"
#export PYTHONPATH="${PYTHONPATH}:."
#CMD="python3 src/BorsdataAPI/borsdata/borsdata_client.py"
#CMD="env"
#CMD="python3 -m site --user-site"
ENV_FILE=".env"

docker run -it \
	--env-file=${ENV_FILE} \
	-e PYTHONPATH=${PYTHONPATH}:/usr/src/app/src/BorsdataAPI/ \
	-v ${PROJECT_DIR}:${DOCKER_DIR} \
	${DOCKER_IMAGE}:latest ${CMD}
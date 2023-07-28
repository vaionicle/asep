IMAGE_NAME := asep_python_311:latest

DOCKER_RUN := docker run -it --rm \
	-v ${PWD}/:/opt/asep \
	-w "/opt/asep" \
	${IMAGE_NAME}

build:
	@echo "build"
	docker build \
		-f ./Dockerfile \
		-t ${IMAGE_NAME} .

ssh:
	${DOCKER_RUN} /bin/sh

extract:
	@echo "extract"


import:
	@echo "Import"
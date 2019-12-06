IMAGE_NAME=jeffrey04/rental-crawler/edgeprop
IMAGE_TAG=20191206

.PHONY: all build clean run

all: clean run

build:
	docker pull jonatkinson/python-poetry:3.7 && \
		docker build --rm -t ${IMAGE_NAME}:${IMAGE_TAG} . && \
		docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest

clean:
	rm -rf ./crawler-data
	docker rmi ${IMAGE_NAME}:latest
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG}

run:
	mkdir -p crawler-data && \
		docker-compose up -d crawler
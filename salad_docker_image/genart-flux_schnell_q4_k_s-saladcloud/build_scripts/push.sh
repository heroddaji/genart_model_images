#!/bin/bash

GENART_DOCKER_IMAGE_VERSION=1.0.2
export GENART_DOCKER_IMAGE_VERSION
docker image push heroddaji/genart-flux_schnell_q4_k_s-saladcloud:$GENART_DOCKER_IMAGE_VERSION

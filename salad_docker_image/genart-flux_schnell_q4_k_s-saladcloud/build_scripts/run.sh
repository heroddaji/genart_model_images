#!/bin/bash

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker run --gpus all -m 12G -p 8188:8188 -p 3000:3000 heroddaji/genart-flux_schnell_q4_k_s-saladcloud:$GENART_DOCKER_IMAGE_VERSION

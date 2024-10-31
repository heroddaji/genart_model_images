#!/bin/bash

/salad-http-job-queue-worker-v004 &
/comfyui-api &
wait -n
exit $?
#!/bin/bash

/salad-http-job-queue-worker &
/comfyui-api &
wait -n
exit $?
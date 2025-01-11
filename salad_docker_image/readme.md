1 - first build the comfyui-api binary, it is the component that will interact receive request from mobile, then interact with comfyui backend API in the docker
2 - copy comfyui-api binnary to genart-flux_schnell_q4_k_s-saladcloud
    the docker image also has salad queue-http binary to interact with salad queue API: https://github.com/SaladTechnologies/salad-cloud-job-queue-worker/releases/tag/v0.4.1
3 - build the docker image, publish
4 - use salad portal to deploy
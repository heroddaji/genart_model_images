ARG comfy_version=0.2.2
ARG api_version=1.4.2
FROM ghcr.io/ai-dock/comfyui:v2-cuda-12.1.1-base-22.04-v${comfy_version}

# Disable the authentication and cloudflare tunnels provided by the base image
ENV WEB_ENABLE_AUTH=false
ENV CF_QUICK_TUNNELS=false

# Disable a bunch of services we don't need for the worker
RUN rm /etc/supervisor/supervisord/conf.d/jupyter.conf
RUN rm /etc/supervisor/supervisord/conf.d/storagemonitor.conf
RUN rm /etc/supervisor/supervisord/conf.d/comfyui_api_wrapper.conf
RUN rm /etc/supervisor/supervisord/conf.d/serviceportal.conf
RUN rm /etc/supervisor/supervisord/conf.d/sshd.conf
RUN rm /etc/supervisor/supervisord/conf.d/syncthing.conf


# Set up some environment variables for the worker
ENV COMFYUI_DIR=/opt/ComfyUI
ENV STARTUP_CHECK_MAX_TRIES=30
ENV MODEL_DIR=/opt/ComfyUI/models
ENV OUTPUT_DIR=/opt/ComfyUI/output
ENV INPUT_DIR=/opt/ComfyUI/input
ENV CUSTOM_NODES_DIR=${COMFYUI_DIR}/custom_nodes
ENV CHECKPOINT_DIR=${MODEL_DIR}/checkpoints
ENV UNET_DIR=${MODEL_DIR}/unet
ENV VAE_DIR=${MODEL_DIR}/vae
ENV CLIP_DIR=${MODEL_DIR}/clip
ENV UPSCALE_DIR=${MODEL_DIR}/upscale_models

# download all of these models from huggingface, and put them in the models directory
COPY models/flux1-schnell-Q4_K_S.gguf ${UNET_DIR}/
COPY models/ae.safetensors ${VAE_DIR}/
COPY models/clip_l.safetensors ${CLIP_DIR}/
COPY models/t5xxl_fp8_e4m3fn.safetensors ${CLIP_DIR}/
COPY models/RealESRGAN_x2.pth ${UPSCALE_DIR}/
COPY models/RealESRGAN_x4.pth ${UPSCALE_DIR}/

# Install the GGUF node
RUN git clone https://github.com/city96/ComfyUI-GGUF ${CUSTOM_NODES_DIR}/ComfyUI-GGUF
RUN /opt/environments/python/comfyui/bin/python -m pip install gguf>=0.9.1

# Install this custom node to save images to webp format
RUN git clone https://github.com/palant/extended-saveimage-comfyui ${CUSTOM_NODES_DIR}/extended-saveimage-comfyui


# We also need to copy the comfyui-api binary into the image, since ComfyUI
# is fully asyncronous by default, and has no convenient way to retrieve 
# generated images. If you're adding a custom worker, you'll need to copy it in here.
COPY comfyui_api_workflows/bin/comfyui-api .
RUN chmod +x comfyui-api

# The comfyui wrapper api supports a warmup mode, where it will run a provided workflow before starting the server.
COPY comfyui_api_workflows/warmup_workflow_api.json .
ENV WARMUP_PROMPT_FILE=warmup_workflow_api.json

# We can add custom endpoints to the comfyui wrapper by poulating a workflows directory.
ENV WORKFLOW_DIR=/workflows
COPY comfyui_api_workflows/workflows ${WORKFLOW_DIR}

COPY comfyui_code_patch/server.py ${COMFYUI_DIR}/

CMD ["./comfyui-api"]

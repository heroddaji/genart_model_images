# We're going to use this verified comfyui image as a base
ARG comfy_version=0.2.2
ARG api_version=1.4.2
FROM saladtechnologies/comfyui:comfy${comfy_version}-api${api_version}-base

ENV COMFYUI_DIR=/opt/ComfyUI
ENV CUSTOM_NODES_DIR=${COMFYUI_DIR}/custom_nodes
ENV CHECKPOINT_DIR=${MODEL_DIR}/checkpoints
ENV UNET_DIR=${MODEL_DIR}/unet
ENV VAE_DIR=${MODEL_DIR}/vae
ENV CLIP_DIR=${MODEL_DIR}/clip

# https://huggingface.co/Comfy-Org/flux1-schnell
COPY models/flux1-schnell-Q4_K_S.gguf ${UNET_DIR}/
COPY models/ae.safetensors ${VAE_DIR}/
COPY models/clip_l.safetensors ${CLIP_DIR}/
COPY models/t5xxl_fp8_e4m3fn.safetensors ${CLIP_DIR}/
# COPY models/v1-5-pruned-emaonly.ckpt ${CHECKPOINT_DIR}/

# The comfyui wrapper api supports a warmup mode, where it will run a provided workflow before starting the server.
COPY models/flux_txt2img_api.json .
ENV WARMUP_PROMPT_FILE=flux_txt2img_api.json

# We can add custom endpoints to the comfyui wrapper by poulating a workflows directory.
ENV WORKFLOW_DIR=/workflows
COPY workflows ${WORKFLOW_DIR}

# Install the GGUF node
RUN git clone https://github.com/city96/ComfyUI-GGUF ${CUSTOM_NODES_DIR}/ComfyUI-GGUF
RUN /opt/environments/python/comfyui/bin/python -m pip install gguf>=0.9.1

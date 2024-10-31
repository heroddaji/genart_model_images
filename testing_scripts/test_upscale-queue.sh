#!/bin/bash

# Convert and encode image to base64
base64_image=$(base64 -w 0 sample_image.webp)
upscale_model="x2"

# Create a temporary JSON payload file
cat > payload.json << EOF
{
  "workflowRoute": "/workflow/upscale/esrgan_upscale",
  "workflowInput": {  
    "input": {
      "image": "${base64_image}",
      "upscale_model": "RealESRGAN_${upscale_model}.pth"
    }
  }
}
EOF

# Use the payload file with curl
curl -X POST "http://127.0.0.1:3000/queue" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @payload.json \
  | tee response_upscale-queue.json

# Extract and decode base64 images
# from the JSON response
jq -r '.images[]' response_upscale-queue.json | while read -r base64_img; do
    echo "$base64_img" | base64 -d > "upscaled_image_${upscale_model}.png"
done


rm payload.json
rm response_upscale-queue.json

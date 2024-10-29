#!/bin/bash

# Convert and encode image to base64
base64_image=$(base64 -w 0 test_image.webp)
upscale_model="x4"

# Create a temporary JSON payload file
cat > payload.json << EOF
{
    "input": {
      "image": "${base64_image}",
      "upscale_model": "RealESRGAN_${upscale_model}.pth"
    }
}
EOF

# Use the payload file with curl
curl -X POST "http://127.0.0.1:3000/workflow/upscale/esrgan_upscale" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @payload.json \
  | tee response_upscale.json

# Extract and decode base64 images
# from the JSON response
jq -r '.images[]' response_upscale.json | while read -r base64_img; do
    echo "$base64_img" | base64 -d > "upscaled_image_${upscale_model}.png"
done



# Clean up the temporary file
rm payload.json


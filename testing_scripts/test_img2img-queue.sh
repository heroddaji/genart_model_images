#!/bin/bash

# Convert and encode image to base64
base64_image=$(base64 -w 0 sample_image.webp)

# Create a temporary JSON payload file
cat > payload.json << EOF
{
  "workflowRoute": "/workflow/flux/img2img",
  "workflowInput": {
    "input": {
      "prompt": "sexy modern woman in bikini in a bottle, pixel art, cute, fantasy, vibrant",
      "image": "${base64_image}"
    }
  }
}
EOF

# Use the payload file with curl
curl -X POST "http://127.0.0.1:3000/queue" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @payload.json \
  | tee response_img2img-queue.json

# Extract and decode base64 images
# from the JSON response
jq -r '.images[]' response_img2img-queue.json | while read -r base64_img; do
    echo "$base64_img" | base64 -d > "img2img_$(date +%s)_$RANDOM.webp"
done

rm response_img2img-queue.json
rm payload.json


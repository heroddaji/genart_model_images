#!/bin/bash

# Convert and encode image to base64
base64_image=$(base64 -w 0 txt2img_1730261239_343.png)
upscale_model="x4"

# Create a temporary JSON payload file
cat > payload.json << EOF
{
    "input": {
      "prompt": "sexy modern woman in bikini, pixel art, cute, fantasy, vibrant",
      "image": "${base64_image}"
    }
}
EOF

# Use the payload file with curl
curl -X POST "http://127.0.0.1:3000/workflow/flux/img2img" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @payload.json \
  | tee response_img2img.json

# Extract and decode base64 images
# from the JSON response
jq -r '.images[]' response_img2img.json | while read -r base64_img; do
    echo "$base64_img" | base64 -d > "img2img_$(date +%s)_$RANDOM.webp"
done



# Clean up the temporary file
rm payload.json


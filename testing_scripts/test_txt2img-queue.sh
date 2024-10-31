#!/bin/bash

cat > payload.json << EOF
{
  "workflowRoute": "/workflow/flux/txt2img",
  "workflowInput": {  
    "input": {
      "prompt": "modern beautiful sorceress, mythp0rt, . magical, fantastical, enchanting, storybook style, highly detailed",
      "batch_size": 2,
      "steps": 5
    }
  }
}
EOF

curl -X POST "http://127.0.0.1:3000/queue" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @payload.json \
  | tee response_txt2img-queue.json

# Extract and decode base64 images from the JSON response
jq -r '.images[]' response_txt2img-queue.json | while read -r base64_img; do
    echo "$base64_img" | base64 -d > "txt2img_$(date +%s)_$RANDOM.png"
done

rm payload.json
rm response_txt2img-queue.json

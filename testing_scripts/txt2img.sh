curl -X POST "http://127.0.0.1:3000/workflow/flux/txt2img" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "fairy tale beautiful sorceress, magical, fantastical, enchanting, storybook style, highly detailed",
      "batch_size": 1,
      "steps": 1
    }
  }' \
  | tee response.json

# Extract and decode base64 images from the JSON response
jq -r '.images[]' response.json | while read -r base64_img; do
    echo "$base64_img" | base64 -d > "image_$(date +%s)_$RANDOM.png"
done
curl -X POST "http://127.0.0.1:3000/workflow/flux/txt2img" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "fantastical, whimsical mushroom house in a lush forest, and a druid in reindeer body walking around",
      "batch_size": 2,
      "steps": 5
    }
  }' \
  | tee response_txt2img.json

# Extract and decode base64 images from the JSON response
jq -r '.images[]' response_txt2img.json | while read -r base64_img; do
    echo "$base64_img" | base64 -d > "image_$(date +%s)_$RANDOM.png"
done


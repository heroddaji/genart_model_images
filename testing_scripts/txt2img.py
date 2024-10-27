import requests
import base64
import json
import random

def test_txt2img_service(
    prompt="fairy tale beautiful sorceress, mythp0rt, . magical, fantastical, enchanting, storybook style, highly detailed",
    batch_size=1,
    steps=5,
    url="http://127.0.0.1:3000/workflow/flux/txt2img"
):
    """
    Test the txt2img service by sending a POST request and saving the resulting images
    """
    # Prepare the request payload
    payload = {
        "input": {
            "prompt": prompt,
            "batch_size": batch_size,
            "steps": steps
        }
    }
    
    # Make the POST request
    response = requests.post(
        url,
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        json=payload
    )
    
    # Check if request was successful
    if response.status_code == 200:
        # Write the full response to a JSON file
        with open('response.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        print("Full response saved to 'response.json'")
        
        # Get all images from the response
        images_data = response.json()['images']
        print(f"Received {len(images_data)} images")
        
        # Save each image with a unique filename
        for i, image_data in enumerate(images_data):
            filename = f'image_{random.randint(1000, 9999)}.png'
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(image_data))
            print(f"Image successfully saved as '{filename}'")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_txt2img_service(
        batch_size=4,
        steps=5
    )

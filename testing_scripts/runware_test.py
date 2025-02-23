import requests
import base64
import uuid  # Import uuid for generating UUID


def send_request(url, image_path):
        try:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            payload = [
                        {
                            "taskType": "authentication",
                            "apiKey": "z2bMgI9UMgVSlQ9SArKwCTHWkrfisUbu"
                        },
                        {
                            "taskType": "imageUpscale",
                            "taskUUID": str(uuid.uuid4()),
                            "inputImage": "https://images.nightcafe.studio/jobs/PB64FDEmq94M26vWBDYy/PB64FDEmq94M26vWBDYy--3--ubt51.jpg",
                            "outputType": "URL",
                            "outputFormat": "WEBP",
                            "upscaleFactor": 4,
                            "includeCost": True
                        }
                    ]

        
            print(payload)
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            print(response.json())  # Assuming the response is in JSON format
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_url = "https://api.runware.ai/v1"  # Replace with your API URL
    image_path = "sample_image.webp"
    send_request(api_url, image_path)  # Replace with the path to your image file
    
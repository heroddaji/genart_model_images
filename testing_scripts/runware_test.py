import requests
import base64
import uuid  

def flux_redux(url, image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
        payload = [
            {
                "taskType": "authentication",
                "apiKey": "z2bMgI9UMgVSlQ9SArKwCTHWkrfisUbu"
            },
            {
                "taskType": "imageInference",
                "taskUUID": str(uuid.uuid4()),
                "model": "runware:101@1",
                "positivePrompt": "cute cat in a  bottle",
                "includeCost": True,
                "seedImage": str('data:image/png;base64,'+image_data),
                "strength": 0.76,
                #"CFGScale": 25,
                "width": 768,
                "height": 1024,
                "steps": 1,
                "scheduler":"DPM++ 2M",
                "ipAdapters": [
                    {
                        "guideImage": "https://raw.githubusercontent.com/heroddaji/genart_production_data/refs/heads/main/testing_images/asiangirl.jpg",                    
                        "model": "runware:105@1",
                        # "weight": 0.7
                    }
                ]
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



def send_img2img_request(url, image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        payload = [
            {
                "taskType": "authentication",
                "apiKey": "z2bMgI9UMgVSlQ9SArKwCTHWkrfisUbu"
            },
            {
                "taskType": "imageInference",
                "taskUUID": str(uuid.uuid4()),
                "outputType": "URL",
                "outputFormat": "WEBP",
                # "CFGScale": 3,
                "clipSkip": 0,
                "positivePrompt": "Close-up shot of a young woman's face and upper torso (anime style:2). She has long, dark brown hair with a slight wave, parted to the side (anime style:2). Her skin is fair with a soft, almost airbrushed appearance (anime style:2). She is wearing makeup: peachy-orange eyeshadow, rosy pink blush high on her cheeks, and a matte coral-orange lipstick (anime style:2). Her eyes are brown and appear slightly enlarged, characteristic of anime style (anime style:2). A white earphone is visible in her right ear, with the wire extending down her chest (anime style:2). She's wearing a light pink or peach-colored blouse with slight ruching at the shoulder (anime style:2). The background is blurred, but shows hints of a green bus seat and a window with blurry trees outside (anime style:2). Focus on capturing the soft lighting and idealized features, typical of (anime style:2) a highly polished anime aesthetic. The perspective is slightly angled downwards. (anime style:2)",
                # "seedImage": "https://raw.githubusercontent.com/heroddaji/genart_production_data/refs/heads/main/testing_images/asiangirl.jpg",
                "seedImage": str('data:image/png;base64,'+image_data),
                "model": "runware:100@1",
                "height": 768,
                "width": 768,
                "strength": 0.8,
                "numberResults": 2,
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

def send_background_removal_request(url, image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        payload = [
             {
                        "taskType": "authentication",
                        "apiKey": "z2bMgI9UMgVSlQ9SArKwCTHWkrfisUbu"
                    },
            {
                "taskType": "imageBackgroundRemoval",
                "taskUUID": str(uuid.uuid4()),
                "imageUUID": str(uuid.uuid4()),
                "inputImage": "https://im.runware.ai/image/ii/4f2d651c-8811-4e05-8a97-997f39ea18d1.WEBP?_gl=1*1ie7ifp*_gcl_au*NDUzNzY5OTExLjE3Mzg1Nzk3NjAuOTU0MDgxODA2LjE3NDAzNTY2ODkuMTc0MDM1NjY5Nw..",
                "outputType": "URL",
                "outputFormat": "WEBP",
                "rgba": [255, 255, 255, 0],
                "postProcessMask": True,
                "returnOnlyMask": False,
                "alphaMatting": True,
                "alphaMattingForegroundThreshold": 240,
                "alphaMattingBackgroundThreshold": 10,
                "alphaMattingErodeSize": 10,
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

def send_scale_request(url, image_path):
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
    image_path = "testing_scripts/sample_image.webp"
    image_path = "testing_scripts/anime1.png"
    # send_scale_request(api_url, image_path)  
    # send_background_removal_request(api_url, image_path) 
    # send_img2img_request(api_url, image_path) 
    flux_redux(api_url,image_path) 
    
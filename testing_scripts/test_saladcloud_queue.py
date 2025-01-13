#!/usr/bin/env python3
import requests
import json
import base64
import time
import os
import random

organization = "nevitech"
project = "genart"
queue = "genart-job-queue"
salad_api_key = "6be3fd2b-c92b-4cd7-a6c2-c6617b9bdfd7"

def generate_salad_queue_payloads(test_image):
    with open(test_image, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    upscale_model = ["RealESRGAN_x2.pth", "RealESRGAN_x4.pth"]
    return {
       "upscale": {
            "input": {
                "workflowRoute": "/workflow/upscale/esrgan_upscale",
                "workflowInput": {
                    "input": {
                        "image": img_base64,
                        "upscale_model": upscale_model[random.randint(0, 1)]
                    }
                }
            }
        }, 
        "txt2img": {
            "input": {
                "workflowRoute": "/workflow/flux/txt2img",
                "workflowInput": {
                    "input": {                        
                        # "prompt": "modern beautiful sorceress, mythp0rt, magical, fantastical, enchanting, storybook style, highly detailed",
                        "prompt": "cute dog running in the park, highly detailed",
                        "batch_size": 4,
                        "steps": 5
                    }
                }
            }
        }, 
        "img2img": {
            "input": {
                "workflowRoute": "/workflow/flux/img2img",
                "workflowInput": {
                    "input": {                        
                        "image": img_base64,
                        "prompt": "a robot dog with eyes shoot our lazer beam, in a cyber punk environment"
                    }
                }
            }
        }, 
    }

def test_img2img_queue(base_url, output_dir, use_salad_queue_api, test_image):
    print("\nTesting img2img workflow...")

    workflow_route = "/workflow/flux/img2img"
    url = f"{base_url}{workflow_route}"

    with open(test_image, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    payload = {
        "input": {
            "image": img_base64,
            "prompt": "cute little girl with a red hat, fairytale, highly detailed",
        }
    }

    if use_salad_queue_api:
        url = f"{base_url}/queue"
        payload = {
            "workflowRoute": workflow_route,
            "workflowInput": payload
        }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    if response.status_code == 200:
        print("img2img test successful")
        result = response.json()
        # Save images
        for i, img_base64 in enumerate(result.get('images', [])):
            img_data = base64.b64decode(img_base64)
            filename = os.path.join(output_dir, f"img2img_{int(time.time())}_{i}.png")
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Saved img2img image: {filename}")
    else:
        print(f"img2img test failed with status code: {response.status_code}")
        print(response.text)


def test_txt2img_queue(base_url, output_dir, use_salad_queue_api):
    print("\nTesting txt2img workflow...")

    workflow_route = "/workflow/flux/txt2img"
    url = f"{base_url}{workflow_route}"

    payload = {
        "input": {
            "prompt": "modern beautiful sorceress, mythp0rt, magical, fantastical, enchanting, storybook style, highly detailed",
            "batch_size": 1,
            "steps": 5
        }
    }

    if use_salad_queue_api:
        url = f"{base_url}/queue"
        payload = {
            "workflowRoute": workflow_route,
            "workflowInput": payload
        }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    if response.status_code == 200:
        print("txt2img test successful")
        result = response.json()
        # Save images
        for i, img_base64 in enumerate(result.get('images', [])):
            img_data = base64.b64decode(img_base64)
            filename = os.path.join(output_dir, f"txt2img_{int(time.time())}_{i}.png")
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Saved txt2img image: {filename}")
    else:
        print(f"txt2img test failed with status code: {response.status_code}")
        print(response.text)

def test_upscale_queue(base_url, output_dir, use_salad_queue_api, test_image):
    print("\nTesting upscale workflow...")

    workflow_route = "/workflow/upscale/esrgan_upscale"
    url = f"{base_url}{workflow_route}"
    upscale_model = ["RealESRGAN_x2.pth", "RealESRGAN_x4.pth"]

    with open(test_image, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    payload = {
        "input": {
            "image": img_base64,
            "upscale_model": upscale_model[random.randint(0, 1)]
        }
    }

    if use_salad_queue_api:
        url = f"{base_url}/queue"
        payload = {
            "workflowRoute": workflow_route,
            "workflowInput": payload
        }
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
    if response.status_code == 200:
        print("upscale test successful")
        result = response.json()
        # Save images
        for i, img_base64 in enumerate(result.get('images', [])):
            img_data = base64.b64decode(img_base64)
            filename = os.path.join(output_dir, f"upscale_{int(time.time())}_{i}.png")
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Saved upscale image: {filename}")
    else:
        print(f"upscale test failed with status code: {response.status_code}")
        print(response.text)

def count_images_in_dir(directory):
    return len([f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.webp'))])

def test_local_queue(base_url, output_dir, use_salad_queue_api, repeat, test_image):
    """Test the SaladCloud queue with multiple requests"""
    print(f"Testing with url: {base_url}, output_dir: {output_dir}, use_salad_queue_api: {use_salad_queue_api}, repeat: {repeat}")

    os.makedirs(output_dir, exist_ok=True)
    
    total_tests = repeat * 3
    for i in range(repeat):
        test_upscale_queue(base_url, output_dir, use_salad_queue_api, test_image)
        test_txt2img_queue(base_url, output_dir, use_salad_queue_api)
        test_img2img_queue(base_url, output_dir, use_salad_queue_api, test_image)    
    
    count_images = count_images_in_dir(output_dir)
    if(count_images == total_tests):
        print(f"All tests passed count: {count_images}/{total_tests}")
    else:
        print(f"Some tests failed count: {count_images}/{total_tests}")

def create_salad_queue_jobs(test_image, output_dir, repeat=1):
    print("Testing SaladCloud queue...")
    job_ids = []

    url = f"https://api.salad.com/api/public/organizations/{organization}/projects/{project}/queues/{queue}/jobs"
    headers = {
        "Salad-Api-Key": salad_api_key,
        "Content-Type": "application/json"
    }
    
    for _ in range(repeat):
        for payload in generate_salad_queue_payloads(test_image).values():
            response = requests.post(url, headers=headers, json=payload)
            job_id = response.json()["id"]
            print(f"Job ID: {job_id}")
            job_ids.append(job_id)

            #save queue output of jobID
            with open(os.path.join(output_dir, f"{job_id}.json"), 'w') as f:
                json.dump(response.json(), f, indent=4)
    
    return job_ids


def get_salad_queue_output(job_ids, output_dir, repeat):
    print(f"Testing get job output for job ID: {job_ids}")  
    
    organization = "nevitech"
    project = "genart"
    queue = "genart-job-queue"

    salad_api_key = "6be3fd2b-c92b-4cd7-a6c2-c6617b9bdfd7"
    headers = {
        "Salad-Api-Key": salad_api_key,
        "Content-Type": "application/json"
    }
    
    count = 0
    job_ids_count = len(job_ids) * repeat
    while True:
        for job_id in job_ids:
            url = f"https://api.salad.com/api/public/organizations/{organization}/projects/{project}/queues/{queue}/jobs/{job_id}"
            get_job_output_response = requests.get(url, headers=headers)
            if get_job_output_response.json()["status"] != "succeeded":
                #save queue output of jobID that is not succeeded yet
                with open(os.path.join(output_dir, f"{job_id}_waiting.json"), 'w') as f:
                    json.dump(get_job_output_response.json(), f, indent=4)

                print(f"job {job_id} not succeeded")
                continue

            if get_job_output_response.status_code == 200:
                os.makedirs(output_dir, exist_ok=True)
                result = get_job_output_response.json()["output"]
                
                #save json output success with images
                with open(os.path.join(output_dir, f"{job_id}_success.json"), 'w') as f:
                    json.dump(get_job_output_response.json(), f, indent=4)

                # Save images
                for i, img_base64 in enumerate(result.get('images', [])):
                    img_data = base64.b64decode(img_base64)
                    filename = os.path.join(output_dir, f"img_{int(time.time())}_{i}.png")
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                    print(f"Saved image: {filename}")
                
                count += 1
                job_ids.remove(job_id)
                print(f"job {job_id} removed, remaining jobs count: {len(job_ids)}")
            else:
                count += 1
                job_ids.remove(job_id)
                print(f"job {job_id} removed, remaining jobs count: {len(job_ids)}")
                print(f"img test failed with status code: {get_job_output_response.status_code}")
            
            if count == job_ids_count:
                return 

            time.sleep(2)


def main():
    print("Starting API tests...")
    ############ test local docker
    #  test_local_queue(
    #     base_url="http://127.0.0.1:3000",
    #     # url="http://127.0.0.1:3000",
    #     output_dir=f"output_{random.randint(0, 1000)}",
    #     use_salad_queue_api=True,
    #     repeat=1,
    #     test_image="sample_image.webp"
    # )



    ########### test online salad queue
    #create output directory
    output_dir = f"output_saladqueue_{random.randint(0, 1000)}"
    os.makedirs(output_dir, exist_ok=True)

    test_image = "sample_image.webp"
    repeat = 2
    job_ids = create_salad_queue_jobs(test_image=test_image, output_dir=output_dir, repeat=repeat)
    get_salad_queue_output(job_ids, output_dir=output_dir, repeat=repeat)

    
if __name__ == "__main__":
    main()

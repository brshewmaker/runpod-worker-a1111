#!/usr/bin/env python3
"""
RunPod A1111 Worker Test Script

This script tests your RunPod A1111 serverless worker by:
1. Listing available models
2. Changing the active model
3. Generating an image and downloading it locally

Usage:
    python test_runpod_a1111.py

Make sure to set your RUNPOD_ENDPOINT_URL and RUNPOD_API_KEY below.
"""

import requests
import base64
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Configuration - UPDATE THESE VALUES
RUNPOD_ENDPOINT_URL = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID"  # Replace with your endpoint URL
RUNPOD_API_KEY = "YOUR_API_KEY"  # Replace with your RunPod API key

class RunPodA1111Client:
    def __init__(self, endpoint_url: str, api_key: str):
        self.endpoint_url = endpoint_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, payload: Dict, use_sync: bool = True) -> Dict:
        """Make a request to the RunPod endpoint"""
        endpoint = "/runsync" if use_sync else "/run"
        url = f"{self.endpoint_url}{endpoint}"
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        
        result = response.json()
        
        # If using async endpoint, poll for completion
        if not use_sync and result.get("status") == "IN_QUEUE":
            return self._poll_for_completion(result["id"])
        
        return result
    
    def _poll_for_completion(self, job_id: str, max_wait: int = 300) -> Dict:
        """Poll for job completion (for async requests)"""
        status_url = f"{self.endpoint_url}/status/{job_id}"
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            response = requests.get(status_url, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            status = result.get("status")
            
            if status == "COMPLETED":
                return result
            elif status == "FAILED":
                raise Exception(f"Job failed: {result}")
            
            print(f"Status: {status}, waiting...")
            time.sleep(5)
        
        raise TimeoutError(f"Job {job_id} did not complete within {max_wait} seconds")
    
    def list_models(self) -> List[Dict]:
        """Get list of available models"""
        payload = {
            "input": {
                "api": {
                    "method": "GET",
                    "endpoint": "/sdapi/v1/sd-models"
                },
                "payload": {}
            }
        }
        
        print("🔍 Fetching available models...")
        result = self._make_request(payload)
        
        if result.get("status") == "COMPLETED":
            models = result.get("output", [])
            print(f"✅ Found {len(models)} models")
            return models
        else:
            raise Exception(f"Failed to get models: {result}")
    
    def set_model(self, model_name: str) -> bool:
        """Change the active model"""
        payload = {
            "input": {
                "api": {
                    "method": "POST",
                    "endpoint": "/sdapi/v1/options"
                },
                "payload": {
                    "sd_model_checkpoint": model_name
                }
            }
        }
        
        print(f"🔄 Switching to model: {model_name}")
        result = self._make_request(payload)
        
        if result.get("status") == "COMPLETED":
            print("✅ Model changed successfully")
            return True
        else:
            raise Exception(f"Failed to set model: {result}")
    
    def generate_image(self, prompt: str, negative_prompt: str = "", 
                      width: int = 512, height: int = 512, steps: int = 20) -> Dict:
        """Generate an image using txt2img"""
        payload = {
            "input": {
                "api": {
                    "method": "POST",
                    "endpoint": "/sdapi/v1/txt2img"
                },
                "payload": {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "width": width,
                    "height": height,
                    "steps": steps,
                    "cfg_scale": 7,
                    "sampler_name": "DPM++ SDE",
                    "scheduler": "automatic",
                    "batch_size": 1,
                    "seed": -1,
                    "restore_faces": False
                }
            }
        }
        
        print(f"🎨 Generating image: '{prompt}'")
        print(f"📐 Size: {width}x{height}, Steps: {steps}")
        
        result = self._make_request(payload)
        
        if result.get("status") == "COMPLETED":
            print("✅ Image generated successfully")
            return result.get("output", {})
        else:
            raise Exception(f"Failed to generate image: {result}")
    
    def save_image(self, base64_image: str, filename: str = "generated_image.png") -> str:
        """Save base64 encoded image to file"""
        try:
            image_data = base64.b64decode(base64_image)
            filepath = Path(filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            print(f"💾 Image saved as: {filepath.absolute()}")
            return str(filepath.absolute())
        except Exception as e:
            raise Exception(f"Failed to save image: {e}")

def main():
    # Validate configuration
    if "YOUR_ENDPOINT_ID" in RUNPOD_ENDPOINT_URL or "YOUR_API_KEY" in RUNPOD_API_KEY:
        print("❌ Please update RUNPOD_ENDPOINT_URL and RUNPOD_API_KEY in the script")
        print("   RUNPOD_ENDPOINT_URL should look like: https://api.runpod.ai/v2/your-endpoint-id")
        return
    
    try:
        client = RunPodA1111Client(RUNPOD_ENDPOINT_URL, RUNPOD_API_KEY)
        
        print("🚀 Testing RunPod A1111 Worker")
        print("=" * 50)
        
        # 1. List available models
        models = client.list_models()
        print("\n📋 Available Models:")
        for i, model in enumerate(models):
            print(f"  {i+1}. {model['model_name']} ({model['title']})")
        
        if not models:
            print("❌ No models found. Make sure you've installed models on your network volume.")
            return
        
        # 2. Select and change model
        print(f"\n🔄 Testing Model Change")
        first_model = models[0]['model_name']
        client.set_model(first_model)
        
        # 3. Generate a test image
        print(f"\n🎨 Testing Image Generation")
        prompt = "a cute cat sitting on a table, digital art, high quality"
        negative_prompt = "blurry, low quality, distorted"
        
        output = client.generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=512,
            height=512,
            steps=20
        )
        
        # 4. Save the generated image
        if "images" in output and output["images"]:
            base64_image = output["images"][0]
            timestamp = int(time.time())
            filename = f"runpod_test_{timestamp}.png"
            
            saved_path = client.save_image(base64_image, filename)
            
            print(f"\n🎉 Test completed successfully!")
            print(f"   Generated image saved to: {saved_path}")
            
            # Show generation info
            if "info" in output:
                try:
                    info = json.loads(output["info"])
                    print(f"   Seed used: {info.get('seed', 'unknown')}")
                    print(f"   Model used: {info.get('Model', 'unknown')}")
                except:
                    pass
        else:
            print("❌ No image data received in response")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your endpoint URL and API key")
        print("2. Ensure your serverless endpoint is running")
        print("3. Verify your network volume is attached and has models installed")

if __name__ == "__main__":
    main()
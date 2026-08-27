#!/usr/bin/env python
"""Test script to check Gemini API connectivity"""
import requests
import base64
import os

# API Configuration
GEMINI_API_KEY = "AIzaSyDuK_zP4jZNA6rt7IuYLl0Zn83Nl2O_3to"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def test_gemini_api():
    """Test Gemini API with a simple text prompt"""
    try:
        print("🔍 Testing Gemini API...")
        
        # Simple text-only test first
        payload = {
            "contents": [{
                "parts": [{"text": "Hello, can you respond with 'API is working'?"}]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 100,
            }
        }
        
        headers = {"Content-Type": "application/json"}
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        print(f"📡 Making request to: {GEMINI_API_URL}")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ API Response: {text_response}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_with_image():
    """Test with a sample image if text test passes"""
    try:
        # Check if there's an uploaded image to test with
        uploads_dir = "static/uploads"
        if os.path.exists(uploads_dir):
            image_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if image_files:
                image_path = os.path.join(uploads_dir, image_files[0])
                print(f"🖼️ Testing with image: {image_path}")
                
                with open(image_path, "rb") as file:
                    image_data = base64.b64encode(file.read()).decode("ascii")
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "What do you see in this image?"},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_data
                                }
                            }
                        ]
                    }],
                    "generationConfig": {
                        "temperature": 0.4,
                        "topK": 32,
                        "topP": 1,
                        "maxOutputTokens": 500,
                    }
                }
                
                headers = {"Content-Type": "application/json"}
                url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
                
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    text_response = result['candidates'][0]['content']['parts'][0]['text']
                    print(f"✅ Image Analysis: {text_response[:200]}...")
                    return True
                else:
                    print(f"❌ Image API Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
            else:
                print("ℹ️ No images found in uploads folder")
        else:
            print("ℹ️ No uploads folder found")
        
        return True
        
    except Exception as e:
        print(f"❌ Image test exception: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("🧪 GEMINI API TEST")
    print("=" * 50)
    
    # Test 1: Simple text
    if test_gemini_api():
        print("\n✅ Text API test passed!")
        
        # Test 2: Image analysis
        print("\n🖼️ Testing image analysis...")
        if test_with_image():
            print("\n✅ All tests passed! API is working correctly.")
        else:
            print("\n⚠️ Image test failed, but text API works.")
    else:
        print("\n❌ API test failed!")
        print("\n🔧 Possible solutions:")
        print("1. Check if API key is valid")
        print("2. Check internet connection")
        print("3. Try regenerating API key at https://makersuite.google.com/app/apikey")
        print("4. Check if you have API quota remaining")
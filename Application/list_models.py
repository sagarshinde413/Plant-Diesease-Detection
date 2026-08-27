#!/usr/bin/env python
"""List available Gemini models"""
import requests

GEMINI_API_KEY = "AIzaSyDuK_zP4jZNA6rt7IuYLl0Zn83Nl2O_3to"

def list_models():
    """List available models"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            models = response.json()
            print("Available models:")
            for model in models.get('models', []):
                name = model.get('name', '')
                supported_methods = model.get('supportedGenerationMethods', [])
                print(f"- {name}")
                print(f"  Methods: {supported_methods}")
                print()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    list_models()
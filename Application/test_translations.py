#!/usr/bin/env python
"""Test script to verify translations are working"""
from app import app

def test_translations():
    """Test if translations are loaded correctly"""
    with app.test_client() as client:
        # Test English (default)
        response = client.get('/')
        assert b'Plant Disease Detection' in response.data
        print("✓ English working")
        
        # Test Hindi
        response = client.get('/set_language/hi')
        response = client.get('/')
        if 'पौधों की बीमारी' in response.data.decode('utf-8'):
            print("✓ Hindi translations working")
        else:
            print("✗ Hindi translations not found")
        
        # Test Marathi
        response = client.get('/set_language/mr')
        response = client.get('/')
        if 'वनस्पती रोग' in response.data.decode('utf-8'):
            print("✓ Marathi translations working")
        else:
            print("✗ Marathi translations not found")

if __name__ == '__main__':
    print("Testing multilanguage support...")
    test_translations()
    print("\nDone! Start the app with: python app.py")

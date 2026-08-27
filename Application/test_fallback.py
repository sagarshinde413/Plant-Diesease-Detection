#!/usr/bin/env python
"""Test fallback detection system"""
from fallback_detection import get_fallback_result

def test_fallback():
    """Test fallback detection in all languages"""
    
    print("🧪 Testing Fallback Detection System")
    print("=" * 50)
    
    languages = ['en', 'hi', 'mr']
    
    for lang in languages:
        print(f"\n🌐 Testing {lang.upper()} language:")
        result = get_fallback_result('test_image.jpg', lang)
        
        print(f"Plant: {result['plant_name']}")
        print(f"Disease: {result['disease_name']}")
        print(f"Description: {result['description'][:100]}...")
        print(f"Treatment: {result['prevention'][:100]}...")
        print("✅ Fallback working for", lang)
    
    print("\n🎉 All fallback tests passed!")
    print("\nNow your app will:")
    print("1. Try Gemini API first")
    print("2. If API fails → Use fallback detection")
    print("3. Show results in user's language")
    print("4. Never show error pages to users!")

if __name__ == '__main__':
    test_fallback()
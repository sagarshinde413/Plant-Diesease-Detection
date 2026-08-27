#!/usr/bin/env python
"""Test script to verify Gemini response translation"""
from deep_translator import GoogleTranslator

def test_translation():
    """Test translation functionality"""
    
    # Sample text from Gemini
    sample_text = "Wheat Leaf Rust, caused by the fungus Puccinia triticina, is a common disease of wheat."
    
    print("Original (English):")
    print(sample_text)
    print("\n" + "="*50 + "\n")
    
    # Test Hindi translation
    try:
        translator_hi = GoogleTranslator(source='en', target='hi')
        hindi_text = translator_hi.translate(sample_text)
        print("Hindi Translation:")
        print(hindi_text)
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Hindi translation error: {e}")
    
    # Test Marathi translation
    try:
        translator_mr = GoogleTranslator(source='en', target='mr')
        marathi_text = translator_mr.translate(sample_text)
        print("Marathi Translation:")
        print(marathi_text)
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Marathi translation error: {e}")
    
    print("✅ Translation test complete!")
    print("\nNow when you:")
    print("1. Select Hindi/Marathi on the home page")
    print("2. Upload a plant image")
    print("3. The Gemini AI response will be automatically translated!")

if __name__ == '__main__':
    print("Testing Gemini Response Translation...\n")
    test_translation()

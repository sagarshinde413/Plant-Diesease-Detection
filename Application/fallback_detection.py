#!/usr/bin/env python
"""Fallback plant disease detection when API fails"""

def get_fallback_result(image_path, user_lang='en'):
    """Provide a fallback result when Gemini API fails"""
    
    # Basic fallback results based on common plant diseases
    fallback_results = {
        'en': {
            'plant_name': 'Plant',
            'plant_scientific_name': 'Unknown Species',
            'disease_name': 'Possible Plant Disease (API Unavailable)',
            'description': '''Plant Analysis: Unable to connect to AI service

Common Plant Issues to Check:
• Leaf spots or discoloration
• Wilting or drooping leaves  
• Unusual growth patterns
• Pest damage or holes in leaves
• Fungal growth or mold

Please consult a local agricultural expert or extension office for proper diagnosis.''',
            'prevention': '''General Plant Care Recommendations:

1. Watering: Ensure proper drainage and avoid overwatering
2. Sunlight: Provide adequate light for your plant type
3. Air Circulation: Ensure good airflow around plants
4. Cleanliness: Remove dead or diseased plant material
5. Fertilization: Use appropriate fertilizers for your plant
6. Monitoring: Check plants regularly for early problem detection

For specific treatment, please visit your local agricultural extension office or consult with a plant specialist.''',
            'image_url': 'none'
        },
        'hi': {
            'plant_name': 'पौधा',
            'plant_scientific_name': 'अज्ञात प्रजाति',
            'disease_name': 'संभावित पौधे की बीमारी (API अनुपलब्ध)',
            'description': '''पौधे का विश्लेषण: AI सेवा से कनेक्ट नहीं हो सका

जांचने योग्य सामान्य पौधों की समस्याएं:
• पत्तियों पर धब्बे या रंग बदलना
• पत्तियों का मुरझाना या लटकना
• असामान्य वृद्धि पैटर्न
• कीट क्षति या पत्तियों में छेद
• फंगल वृद्धि या मोल्ड

कृपया उचित निदान के लिए स्थानीय कृषि विशेषज्ञ या विस्तार कार्यालय से सलाह लें।''',
            'prevention': '''सामान्य पौधों की देखभाल की सिफारिशें:

1. पानी देना: उचित जल निकासी सुनिश्चित करें और अधिक पानी से बचें
2. धूप: अपने पौधे के प्रकार के लिए पर्याप्त प्रकाश प्रदान करें
3. हवा का संचार: पौधों के चारों ओर अच्छा वायु प्रवाह सुनिश्चित करें
4. सफाई: मृत या रोगग्रस्त पौधे की सामग्री को हटा दें
5. उर्वरीकरण: अपने पौधे के लिए उपयुक्त उर्वरकों का उपयोग करें
6. निगरानी: समस्या की शुरुआती पहचान के लिए नियमित रूप से पौधों की जांच करें

विशिष्ट उपचार के लिए, कृपया अपने स्थानीय कृषि विस्तार कार्यालय में जाएं या पौधे के विशेषज्ञ से सलाह लें।''',
            'image_url': 'none'
        },
        'mr': {
            'plant_name': 'वनस्पती',
            'plant_scientific_name': 'अज्ञात प्रजाती',
            'disease_name': 'संभाव्य वनस्पती रोग (API अनुपलब्ध)',
            'description': '''वनस्पतीचे विश्लेषण: AI सेवेशी कनेक्ट होऊ शकले नाही

तपासण्यायोग्य सामान्य वनस्पतींच्या समस्या:
• पानांवर डाग किंवा रंग बदलणे
• पानांचे कोमेजणे किंवा लटकणे
• असामान्य वाढीचे नमुने
• कीड नुकसान किंवा पानांमध्ये छिद्रे
• बुरशीची वाढ किंवा मोल्ड

योग्य निदानासाठी कृपया स्थानिक कृषी तज्ञ किंवा विस्तार कार्यालयाचा सल्ला घ्या।''',
            'prevention': '''सामान्य वनस्पती काळजीच्या शिफारसी:

1. पाणी देणे: योग्य पाणी निचरा सुनिश्चित करा आणि जास्त पाणी टाळा
2. सूर्यप्रकाश: तुमच्या वनस्पतीच्या प्रकारासाठी पुरेसा प्रकाश द्या
3. हवेचे संचलन: वनस्पतींभोवती चांगला हवेचा प्रवाह सुनिश्चित करा
4. स्वच्छता: मृत किंवा रोगग्रस्त वनस्पती सामग्री काढून टाका
5. खत देणे: तुमच्या वनस्पतीसाठी योग्य खते वापरा
6. निरीक्षण: समस्येच्या लवकर ओळखीसाठी नियमितपणे वनस्पतींची तपासणी करा

विशिष्ट उपचारासाठी, कृपया तुमच्या स्थानिक कृषी विस्तार कार्यालयात भेट द्या किंवा वनस्पती तज्ञाचा सल्ला घ्या।''',
            'image_url': 'none'
        }
    }
    
    return fallback_results.get(user_lang, fallback_results['en'])
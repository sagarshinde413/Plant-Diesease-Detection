import os
from flask import Flask, redirect, render_template, request, jsonify, session
from flask_babel import Babel, gettext, get_locale
import requests
import base64
from deep_translator import GoogleTranslator
from fertilizer_shop import (
    get_recommended_products, 
    get_all_products, 
    get_product_by_id,
    add_to_cart,
    get_cart_items,
    clear_cart
)
from disease_images import get_disease_image_url
from fallback_detection import get_fallback_result


# Google Gemini API Configuration
GEMINI_API_KEY = "AIzaSyDuK_zP4jZNA6rt7IuYLl0Zn83Nl2O_3to"  # Your Gemini API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def detect_disease_with_gemini(image_path):
    """Identify plant and disease using Google Gemini Vision API"""
    try:
        with open(image_path, "rb") as file:
            image_data = base64.b64encode(file.read()).decode("ascii")
        
        prompt = """Analyze this plant/crop image and provide detailed information in JSON format:
{
  "plant_name": "scientific name of the plant",
  "common_name": "common name of the plant (e.g., Sugarcane, Rice, Wheat, Tomato)",
  "disease_name": "specific name of the disease if any, or 'Healthy Plant' if no disease detected",
  "disease_description": "detailed description of the disease, its symptoms, and how it affects the plant",
  "treatment": "comprehensive treatment and prevention methods with specific steps",
  "confidence": "your confidence level as a number between 0-100"
}

Important:
- Focus on agricultural crops and common plants
- Be very specific about disease names (e.g., "Rust", "Leaf Blight", "Powdery Mildew")
- Provide practical treatment advice
- If the plant looks healthy, say so clearly"""

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
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
                "maxOutputTokens": 2048,
            }
        }
        
        headers = {"Content-Type": "application/json"}
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        print(f"🔍 Analyzing image with Gemini AI...")
        print(f"📡 API URL: {GEMINI_API_URL}")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Response Body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            
            # Extract JSON from response
            import json
            import re
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                print(f"✅ Identified: {data.get('common_name')} - {data.get('disease_name')}")
                return data
            else:
                print(f"⚠️ Could not parse JSON from response")
                return None
        elif response.status_code == 400:
            print(f"❌ API Error: Invalid API key or request format")
            return {'error': 'invalid_key'}
        elif response.status_code == 429:
            print(f"❌ API Quota Exceeded: {response.status_code}")
            return {'error': 'quota_exceeded', 'status': response.status_code}
        else:
            print(f"❌ Gemini API Error: {response.status_code} - {response.text}")
            return {'error': 'api_error', 'status': response.status_code}
            
    except Exception as e:
        print(f"❌ Error with Gemini API: {str(e)}")
        return {'error': 'exception', 'message': str(e)}


def detect_disease_with_api(image_path):
    """Detect plant disease using Google Gemini Vision API"""
    try:
        # Check if API key is configured
        if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            return {
                'error': 'no_api_key',
                'message': 'Gemini API key not configured. Please add your API key to app.py'
            }
        
        # Use Gemini AI for detection
        gemini_result = detect_disease_with_gemini(image_path)
        
        # Check for errors
        if gemini_result and 'error' in gemini_result:
            return gemini_result
        
        # Parse and return result
        if gemini_result:
            # Store original Gemini data in session for language switching
            session['original_gemini_data'] = gemini_result
            return parse_gemini_response(gemini_result)
        else:
            # Use fallback detection when Gemini fails
            print("⚠️ Gemini failed, using fallback detection")
            user_lang = session.get('language', 'en')
            fallback_result = get_fallback_result('', user_lang)
            session['original_gemini_data'] = None  # No Gemini data available
            return fallback_result
            
    except Exception as e:
        print(f"❌ Error in detection: {str(e)}")
        return {'error': 'exception', 'message': f'Error: {str(e)}'}


def get_similar_disease_image(plant_name, disease_name):
    """Get similar disease image from curated database"""
    try:
        # Check our curated database first
        image_url = get_disease_image_url(plant_name, disease_name)
        
        if image_url:
            print(f"📸 Found disease image in database: {image_url}")
            return image_url
        else:
            print(f"ℹ️ No image in database for {plant_name} {disease_name}")
            print(f"💡 You can add it to Application/disease_images.py")
            return 'none'
            
    except Exception as e:
        print(f"⚠️ Error getting disease image: {str(e)}")
        return 'none'


def translate_text(text, target_lang):
    """Translate text to target language"""
    if target_lang == 'en' or not text:
        return text
    
    try:
        # Map language codes
        lang_map = {'hi': 'hi', 'mr': 'mr'}
        target = lang_map.get(target_lang, 'en')
        
        if target == 'en':
            return text
        
        # Translate using Google Translator
        translator = GoogleTranslator(source='en', target=target)
        
        # Split long text into chunks (Google Translate has limits)
        max_length = 4500
        if len(text) <= max_length:
            translated = translator.translate(text)
            return translated
        else:
            # Split by paragraphs and translate
            paragraphs = text.split('\n\n')
            translated_paragraphs = []
            for para in paragraphs:
                if para.strip():
                    translated_para = translator.translate(para)
                    translated_paragraphs.append(translated_para)
            return '\n\n'.join(translated_paragraphs)
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails


def parse_gemini_response(gemini_data):
    """Parse Gemini AI response and translate based on user's language"""
    try:
        plant_name = gemini_data.get('plant_name', 'Unknown Plant')
        common_name = gemini_data.get('common_name', plant_name)
        disease_name = gemini_data.get('disease_name', 'Unknown Disease')
        disease_desc = gemini_data.get('disease_description', 'No description available')
        treatment = gemini_data.get('treatment', 'Consult an agricultural expert')
        confidence = gemini_data.get('confidence', 0)
        
        # Get user's selected language
        user_lang = session.get('language', 'en')
        print(f"🌐 User language: {user_lang}")
        
        # Get similar disease image
        print(f"🔍 Searching for similar images: {common_name} - {disease_name}")
        similar_image = get_similar_disease_image(common_name, disease_name)
        print(f"✅ Similar image URL: {similar_image}")
        
        # Translate if needed
        if user_lang != 'en':
            print(f"🔄 Translating to {user_lang}...")
            plant_name = translate_text(plant_name, user_lang)
            common_name = translate_text(common_name, user_lang)
            disease_name = translate_text(disease_name, user_lang)
            disease_desc = translate_text(disease_desc, user_lang)
            treatment = translate_text(treatment, user_lang)
        
        # Create comprehensive description
        if user_lang == 'hi':
            description = f'पहचाना गया पौधा: {common_name} ({plant_name})\n\n'
            description += f'पता लगाई गई बीमारी: {disease_name} ({confidence}% विश्वास)\n\n'
            description += f'विवरण: {disease_desc}'
            prevention = f'{common_name} पर {disease_name} का उपचार:\n\n{treatment}'
        elif user_lang == 'mr':
            description = f'ओळखली गेलेली वनस्पती: {common_name} ({plant_name})\n\n'
            description += f'शोधलेला रोग: {disease_name} ({confidence}% विश्वास)\n\n'
            description += f'वर्णन: {disease_desc}'
            prevention = f'{common_name} वर {disease_name} चा उपचार:\n\n{treatment}'
        else:
            description = f'Plant Identified: {common_name} ({plant_name})\n\n'
            description += f'Disease Detected: {disease_name} ({confidence}% confidence)\n\n'
            description += f'Description: {disease_desc}'
            prevention = f'Treatment for {disease_name} on {common_name}:\n\n{treatment}'
        
        return {
            'plant_name': common_name,
            'plant_scientific_name': plant_name,
            'disease_name': f'{disease_name} ({confidence}% confidence)' if user_lang == 'en' else f'{disease_name} ({confidence}% विश्वास)' if user_lang == 'hi' else f'{disease_name} ({confidence}% विश्वास)',
            'description': description,
            'prevention': prevention,
            'image_url': similar_image
        }
    except Exception as e:
        print(f"Error parsing Gemini response: {str(e)}")
        return None



    except:
        return text


app = Flask(__name__)
app.secret_key = 'plant_disease_detection_secret_key_2025'

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
babel = Babel(app)

def get_locale():
    # Check if language is set in session
    if 'language' in session:
        return session['language']
    # Check if language is in query parameter
    lang = request.args.get('lang')
    if lang in ['en', 'hi', 'mr']:
        session['language'] = lang
        return lang
    # Default to English
    return 'en'

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_locale():
    """Make get_locale available in templates"""
    return dict(get_locale=get_locale)

@app.route('/set_language/<language>')
def set_language(language):
    """Set the language preference"""
    if language in ['en', 'hi', 'mr']:
        session['language'] = language
    return redirect(request.referrer or '/')


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/contact')
def contact():
    return render_template('contact-us.html')


@app.route('/index')
def ai_engine_page():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    # Handle GET request - check if we have cached results
    if request.method == 'GET':
        if 'last_result' in session:
            result = session['last_result']
            # Re-translate based on current language
            user_lang = session.get('language', 'en')
            
            # Get the original English data from session
            if 'original_gemini_data' in session:
                gemini_data = session['original_gemini_data']
                # Re-parse with current language
                api_result = parse_gemini_response(gemini_data)
                
                if api_result:
                    recommended_products = get_recommended_products(api_result['disease_name'])
                    return render_template('submit.html',
                                         plant_name=api_result.get('plant_name', ''),
                                         plant_scientific_name=api_result.get('plant_scientific_name', ''),
                                         title=api_result['disease_name'],
                                         desc=api_result['description'],
                                         prevent=api_result['prevention'],
                                         image_url=api_result['image_url'],
                                         uploaded_image=result.get('uploaded_image', ''),
                                         recommended_products=recommended_products)
        
        # No cached results, redirect to detection page
        return redirect('/index')
    
    # Handle POST request
    if request.method == 'POST':
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            return render_template('error.html',
                                 error_title="API Key Not Configured",
                                 error_message="Please add your Google Gemini API key to app.py",
                                 error_solution="Get a free API key from https://makersuite.google.com/app/apikey")
        
        if 'image' not in request.files:
            return render_template('error.html',
                                 error_title="No Image Uploaded",
                                 error_message="Please select an image file to upload.",
                                 error_solution="Go back and choose a plant/leaf image.")
        
        image = request.files['image']
        
        if image.filename == '':
            return render_template('error.html',
                                 error_title="No Image Selected",
                                 error_message="Please select an image file to upload.",
                                 error_solution="Go back and choose a plant/leaf image.")
        
        filename = image.filename
        file_path = os.path.join('static', 'uploads', filename)
        os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
        image.save(file_path)
        
        api_result = detect_disease_with_api(file_path)
        
        # Check if API returned an error - use fallback instead of error page
        if api_result and 'error' in api_result:
            print(f"⚠️ API Error: {api_result['error']}, using fallback detection")
            
            # Use fallback detection when API fails
            user_lang = session.get('language', 'en')
            api_result = get_fallback_result(file_path, user_lang)
            
            # Add a note that this is fallback detection
            if user_lang == 'hi':
                api_result['disease_name'] = f"सामान्य विश्लेषण (AI अनुपलब्ध)"
            elif user_lang == 'mr':
                api_result['disease_name'] = f"सामान्य विश्लेषण (AI अनुपलब्ध)"
            else:
                api_result['disease_name'] = f"General Analysis (AI Unavailable)"
        
        if api_result:
            # Store result info in session for language switching
            session['last_result'] = {
                'uploaded_image': file_path
            }
            
            # Get recommended products from our shop
            recommended_products = get_recommended_products(api_result['disease_name'])
            
            return render_template('submit.html',
                                 plant_name=api_result.get('plant_name', ''),
                                 plant_scientific_name=api_result.get('plant_scientific_name', ''),
                                 title=api_result['disease_name'],
                                 desc=api_result['description'],
                                 prevent=api_result['prevention'],
                                 image_url=api_result['image_url'],
                                 uploaded_image=file_path,
                                 recommended_products=recommended_products)
        else:
            return render_template('error.html',
                                 error_title="Detection Failed",
                                 error_message="Unable to detect disease. The API returned no results.",
                                 error_solution="Please try again with a clearer image of the plant or leaf.")


@app.route('/shop')
def shop():
    """Fertilizer shop page"""
    products = get_all_products()
    return render_template('shop.html', products=products)


@app.route('/product/<product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = get_product_by_id(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    return redirect('/shop')


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart_route():
    """Add product to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if product_id:
        add_to_cart(product_id, quantity)
        return jsonify({'success': True, 'message': 'Product added to cart'})
    return jsonify({'success': False, 'message': 'Invalid product'})


@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items, total = get_cart_items()
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout')
def checkout():
    """Checkout page"""
    cart_items, total = get_cart_items()
    return render_template('checkout.html', cart_items=cart_items, total=total)


@app.route('/order_success', methods=['POST'])
def order_success():
    """Order confirmation"""
    clear_cart()
    return render_template('order_success.html')


# Keep market route for backward compatibility
@app.route('/market')
def market():
    return redirect('/shop')


if __name__ == '__main__':
    app.run(debug=True)

# Fertilizer Shop Database
# This contains all products available in our shop

FERTILIZERS = {
    'fungicide': {
        'id': 'FUNG001',
        'name': 'Organic Fungicide Pro',
        
        
        'price': 299,
        'currency': '₹',
        'description': 'Broad-spectrum organic fungicide for all plant diseases',
        
        
        'image': 'https://m.media-amazon.com/images/I/61nG+QQNFNL._AC_UF1000,1000_QL80_.jpg',
        'stock': 50,
        'rating': 4.5,
        'uses': ['Rust', 'Blight', 'Mildew', 'Leaf Spot', 'Rot']
    },
    'fertilizer_general': {
        'id': 'FERT001',
        'name': 'NPK Complete Fertilizer',
        
        
        'price': 249,
        'currency': '₹',
        'description': 'Balanced NPK fertilizer for healthy plant growth',
        
        
        'image': 'https://m.media-amazon.com/images/I/71qvGPaHURL._AC_UF1000,1000_QL80_.jpg',
        'stock': 100,
        'rating': 4.7,
        'uses': ['Healthy Plants', 'Growth', 'Flowering', 'Fruiting']
    },
    'pesticide': {
        'id': 'PEST001',
        'name': 'Neem Oil Pesticide',
        
        
        'price': 199,
        'currency': '₹',
        'description': 'Natural neem oil for pest control and disease prevention',
        
        
        'image': 'https://m.media-amazon.com/images/I/61YqH8ZZPNL._AC_UF1000,1000_QL80_.jpg',
        'stock': 75,
        'rating': 4.6,
        'uses': ['Pest Control', 'Disease Prevention', 'Organic']
    },
    'copper_fungicide': {
        'id': 'FUNG002',
        'name': 'Copper Fungicide Spray',
        
        
        'price': 349,
        'currency': '₹',
        'description': 'Copper-based fungicide for bacterial and fungal diseases',
        
        
        'image': 'https://m.media-amazon.com/images/I/71K8zHQqZyL._AC_UF1000,1000_QL80_.jpg',
        'stock': 60,
        'rating': 4.4,
        'uses': ['Bacterial Spot', 'Blight', 'Rust', 'Mildew']
    },
    'organic_compost': {
        'id': 'FERT002',
        'name': 'Premium Organic Compost',
        
        
        'price': 179,
        'currency': '₹',
        'description': 'Rich organic compost for soil health and plant nutrition',
        
        
        'image': 'https://m.media-amazon.com/images/I/81qYYZZGZBL._AC_UF1000,1000_QL80_.jpg',
        'stock': 120,
        'rating': 4.8,
        'uses': ['Soil Health', 'Organic Farming', 'All Plants']
    },
    'bio_fertilizer': {
        'id': 'FERT003',
        'name': 'Bio Fertilizer Mix',
        
        
        'price': 229,
        'currency': '₹',
        'description': 'Beneficial microorganisms for plant growth and disease resistance',
        
        
        'image': 'https://m.media-amazon.com/images/I/71xH8ZZQZPL._AC_UF1000,1000_QL80_.jpg',
        'stock': 80,
        'rating': 4.5,
        'uses': ['Growth Booster', 'Disease Resistance', 'Organic']
    }
}

# Shopping cart (in-memory for demo, use database in production)
shopping_cart = {}

def get_recommended_products(disease_name):
    """Get recommended products based on disease"""
    disease_lower = disease_name.lower()
    recommended = []
    
    # Disease-specific recommendations
    if any(word in disease_lower for word in ['rust', 'blight', 'spot', 'rot', 'mildew']):
        recommended.append(FERTILIZERS['fungicide'])
        recommended.append(FERTILIZERS['copper_fungicide'])
    
    if 'bacterial' in disease_lower:
        recommended.append(FERTILIZERS['copper_fungicide'])
        recommended.append(FERTILIZERS['pesticide'])
    
    if 'healthy' in disease_lower:
        recommended.append(FERTILIZERS['fertilizer_general'])
        recommended.append(FERTILIZERS['organic_compost'])
    
    # Always add general products
    if len(recommended) < 3:
        recommended.append(FERTILIZERS['bio_fertilizer'])
        recommended.append(FERTILIZERS['pesticide'])
    
    # Remove duplicates and limit to 3
    seen = set()
    unique_recommended = []
    for item in recommended:
        if item['id'] not in seen:
            seen.add(item['id'])
            unique_recommended.append(item)
            if len(unique_recommended) >= 3:
                break
    
    return unique_recommended

def get_all_products():
    """Get all products for shop page"""
    return list(FERTILIZERS.values())

def get_product_by_id(product_id):
    """Get specific product by ID"""
    for product in FERTILIZERS.values():
        if product['id'] == product_id:
            return product
    return None

def add_to_cart(product_id, quantity=1):
    """Add product to cart"""
    if product_id in shopping_cart:
        shopping_cart[product_id] += quantity
    else:
        shopping_cart[product_id] = quantity
    return shopping_cart

def get_cart_items():
    """Get all items in cart with details"""
    cart_items = []
    total = 0
    for product_id, quantity in shopping_cart.items():
        product = get_product_by_id(product_id)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    return cart_items, total

def clear_cart():
    """Clear shopping cart"""
    shopping_cart.clear()

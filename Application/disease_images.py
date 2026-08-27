"""
Manual database of plant disease images
Add your own image URLs here for accurate disease reference images
"""

DISEASE_IMAGE_DATABASE = {
    # Sugarcane diseases
    "sugarcane_rust": "https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/PublishingImages/SugarcaneRust01.jpg",
    "sugarcane_red_rot": "https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/PublishingImages/SugarcaneRedRot01.jpg",
    "sugarcane_smut": "https://www.apsnet.org/edcenter/disandpath/fungalbasidio/pdlessons/PublishingImages/SugarcaneSmut01.jpg",
    
    # Rice diseases
    "rice_blast": "https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/PublishingImages/RiceBlast01.jpg",
    "rice_brown_spot": "https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/PublishingImages/RiceBrownSpot01.jpg",
    
    # Wheat diseases
    "wheat_rust": "https://www.apsnet.org/edcenter/disandpath/fungalbasidio/pdlessons/PublishingImages/WheatStemRust01.jpg",
    "wheat_leaf_rust": "https://www.apsnet.org/edcenter/disandpath/fungalbasidio/pdlessons/PublishingImages/WheatLeafRust01.jpg",
    
    # Tomato diseases
    "tomato_blight": "https://www.apsnet.org/edcenter/disandpath/oomycete/pdlessons/PublishingImages/TomatoLateBlight01.jpg",
    "tomato_early_blight": "https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/PublishingImages/TomatoEarlyBlight01.jpg",
    
    # Potato diseases
    "potato_late_blight": "https://www.apsnet.org/edcenter/disandpath/oomycete/pdlessons/PublishingImages/PotatoLateBlight01.jpg",
    
    # Corn/Maize diseases
    "corn_rust": "https://www.apsnet.org/edcenter/disandpath/fungalbasidio/pdlessons/PublishingImages/CornCommonRust01.jpg",
    "corn_leaf_blight": "https://www.apsnet.org/edcenter/disandpath/fungalasco/pdlessons/PublishingImages/CornNorthernLeafBlight01.jpg",
    
    # Add more as needed...
}


def get_disease_image_url(plant_name, disease_name):
    """
    Get disease image URL from database
    Returns None if not found
    """
    # Normalize names
    plant = plant_name.lower().replace(' ', '_')
    disease = disease_name.lower().replace(' ', '_')
    
    # Try exact match
    key = f"{plant}_{disease}"
    if key in DISEASE_IMAGE_DATABASE:
        return DISEASE_IMAGE_DATABASE[key]
    
    # Try partial matches
    for db_key, url in DISEASE_IMAGE_DATABASE.items():
        if plant in db_key and disease in db_key:
            return url
        if disease in db_key:  # Match disease name at least
            return url
    
    return None


def add_disease_image(plant_name, disease_name, image_url):
    """
    Add a new disease image to the database
    Usage: add_disease_image("Sugarcane", "Rust", "https://...")
    """
    key = f"{plant_name.lower().replace(' ', '_')}_{disease_name.lower().replace(' ', '_')}"
    DISEASE_IMAGE_DATABASE[key] = image_url
    print(f"✅ Added: {key} -> {image_url}")

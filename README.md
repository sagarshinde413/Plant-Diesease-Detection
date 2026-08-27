# 🌿 Plant Disease Detection System

AI-powered universal plant disease detection for **ALL plant species worldwide** using Plant.id API.

## ✨ Features

- 🌍 **Universal Detection** - Works with ALL plant species (10,000+ plants)
- 🤖 **AI-Powered** - Advanced disease detection using Plant.id API
- 🌐 **Auto-Translation** - Descriptions automatically translated to Hindi & Marathi
- 🎨 **Modern UI** - Custom CSS with smooth animations
- 💊 **Treatment Plans** - Detailed cure and prevention recommendations
- 📸 **Image Display** - Shows your uploaded image + similar disease examples
- 📱 **Responsive** - Works on desktop, tablet, and mobile

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd Application
pip install flask requests
```

### 2. Get Free API Key
1. Visit [Plant.id](https://web.plant.id/)
2. Sign up (free - 100 detections/month)
3. Copy your API key from dashboard

### 3. Configure API Key
Edit `Application/app.py` (Line 7):
```python
PLANT_ID_API_KEY = "paste_your_api_key_here"
```

### 4. Run Application
```bash
python app.py
```

### 5. Open Browser
```
http://localhost:5000
```

## 📸 How It Works

1. **Upload** - Select a plant/leaf image
2. **Detect** - AI analyzes the image via Plant.id API
3. **Results** - View disease name, description, treatment
4. **Translate** - Switch language (English/Hindi/Marathi)
5. **Buy** - Get product recommendations with purchase links

## 🎯 What's Fixed

✅ **Uploaded Image Display** - Your image now shows correctly
✅ **Relevant Reference Images** - Only shows similar disease examples from API
✅ **Auto-Translation** - Description & treatment auto-translate to Hindi/Marathi
✅ **Clean Project** - Removed unnecessary files and dependencies
✅ **API-Only** - No local model, works purely with Plant.id API

## 🛠️ Technology Stack

- **Backend:** Flask (Python)
- **API:** Plant.id Health Assessment API
- **Translation:** Google Translate API
- **Frontend:** Custom HTML/CSS/JavaScript
- **Design:** Modern gradients, animations, responsive

## 📁 Project Structure

```
Plant_Disease_Detection/
├── Application/
│   ├── app.py                 # Main Flask app (API + Translation)
│   ├── requirements.txt       # Dependencies
│   ├── templates/             # HTML templates
│   │   ├── base.html         # Base layout with navigation
│   │   ├── home.html         # Landing page
│   │   ├── index.html        # Upload page
│   │   ├── submit.html       # Results page (with translation)
│   │   ├── error.html        # Error handling
│   │   ├── contact-us.html   # Contact page
│   │   └── market.html       # Marketplace
│   └── static/
│       ├── images/           # Static images
│       └── uploads/          # User uploaded images
└── README.md
```

## 🌐 Language Support

The system automatically translates disease descriptions and treatments:
- 🇬🇧 **English** - Original from API
- 🇮🇳 **हिंदी (Hindi)** - Auto-translated
- 🇮🇳 **मराठी (Marathi)** - Auto-translated

Switch languages using the dropdown in navigation.

## 🐛 Troubleshooting

**API Key Error**
- Add your Plant.id API key to `app.py` line 7



**Image Not Showing**
- Check `static/uploads/` folder exists
- Verify file permissions

**Detection Failed**
- Check internet connection
- Verify API key is correct
- Try a clearer image
- Check free tier limit (100/month)

## 📝 Dependencies

```
flask>=2.0.0          # Web framework
requests>=2.27.0      # API calls
```

## 👥 Contributors

- **Sagar Shinde** - AI & Machine Learning
- **Vinay Patil** - Full Stack & Cloud Development

## 📞 Contact

Visit the Contact Us page in the application for developer information.

## 🙏 Acknowledgments

- [Plant.id](https://web.plant.id/) for the amazing plant disease detection API
- Google Translate for multilanguage support

---

Made with ❤️ for farmers and plant enthusiasts worldwide 🌱

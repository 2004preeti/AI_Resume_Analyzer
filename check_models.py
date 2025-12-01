import google.generativeai as genai

# Apna API key yaha daalein
API_KEY = "AIzaSyDrQa0lh25LMg5GfccSVnX_DlHgDpSmxgg"  # Your actual key here

try:
    genai.configure(api_key=API_KEY)
    print("✅ Connected to Gemini API")
    
    # List all available models
    models = genai.list_models()
    
    print("\n📋 Available Models for generateContent:")
    print("=" * 60)
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            model_name = model.name
            display_name = model.display_name
            print(f"✓ {display_name}")
            print(f"  Use this name: '{model_name}'")
            print()
            
except Exception as e:
    print(f"❌ Error: {e}")
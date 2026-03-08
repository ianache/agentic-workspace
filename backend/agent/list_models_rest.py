import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file.")
else:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    print(f"Requesting models for API Key (masked)...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models = response.json().get('models', [])
            for m in models:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    print(f"- {m.get('name')} (Display Name: {m.get('displayName')})")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error listing models via REST: {e}")

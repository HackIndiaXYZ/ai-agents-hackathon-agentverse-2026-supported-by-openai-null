import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")

headers = {"Authorization": f"Bearer {key}"}
response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)

if response.status_code == 200:
    models = response.json().get("data", [])
    print("✅ Active models on your Groq key:\n")
    for m in models:
        print(f" - {m['id']}")
else:
    print("❌ Failed to fetch models:", response.status_code, response.text)
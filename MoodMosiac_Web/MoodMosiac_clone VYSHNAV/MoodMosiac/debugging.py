import os

# Assuming your API key is stored in an environment variable named GEMINI_API_KEY
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print(f"Your API Key: {api_key}")
else:
    print("API Key not found. Please set the environment variable 'GEMINI_API_KEY'.")
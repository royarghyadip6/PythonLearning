"""
Gemini Agent integration with code

"""
import os
import certifi
import httpx
from google import genai

api=os.getenv("GEMINI_API_KEY")
# Initialize Gemini client
client = genai.Client(api_key=api)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="what is the daily Gemini API call limit?",
)
print(response.text)
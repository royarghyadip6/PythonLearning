"""
First AI Agent using grok API
https://console.groq.com/docs/
"""
import os

import certifi
import httpx
from groq import Groq

# Create HTTP client with SSL verification disabled (Not secure)
# HTTP_CLIENT = httpx.Client(verify=False)

# Create HTTP client with SSL verification
HTTP_CLIENT = httpx.Client(
    verify=True,
    timeout=60.0,
    proxy = "http://135.245.192.7:8000"
)

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client = HTTP_CLIENT
)

# Use a CURRENT supported model
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "give the info about the user"}
    ]
)

print(response.choices[0].message.content)

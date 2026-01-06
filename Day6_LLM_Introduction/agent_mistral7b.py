"""
visit for api ref https://platform.qubrid.com/
"""
import os

import requests
import json
from pprint import pprint

URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
MISTRAL7B_API_KEY = os.getenv("QUBRID_MISTRAL7B_API_KEY")
headers = {
  "Authorization": f"Bearer {MISTRAL7B_API_KEY}",
  "Content-Type": "application/json"
}

data = {
  "model": "mistralai/Mistral-7B-Instruct-v0.3",
  "messages": [
    {
      "role": "user",
      "content": "Explain quantum computing simply in 3 4 line"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 4096,
  "stream": False,
  "top_p": 1
}

response = requests.post(URL, headers=headers, data=json.dumps(data))

pprint(response.json())
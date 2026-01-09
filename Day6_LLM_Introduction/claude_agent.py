"""
https://platform.claude.com/docs/en/build-with-claude/working-with-messages
"""
import os

import anthropic
import httpx

# Basic request and response
API = os.getenv("CLAUDE_API_KEY")
HTTP_CLIENT = httpx.Client(
    verify=True,
    timeout=60.0,
    proxy = "http://135.245.192.7:8000"
)
message = anthropic.Anthropic(api_key=API , http_client=HTTP_CLIENT).messages.create(
    model="claude-sonnet-4",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message)



# Multiple conversational turns

# message = anthropic.Anthropic().messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1024,
#     messages=[
#         {"role": "user", "content": "Hello, Claude"},
#         {"role": "assistant", "content": "Hello!"},
#         {"role": "user", "content": "Can you describe LLMs to me?"}
#     ],
# )
# print(message)



# Putting words in Claude's mouth

# message = anthropic.Anthropic().messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1,
#     messages=[
#         {"role": "user", "content": "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"},
#         {"role": "assistant", "content": "The answer is ("}
#     ]
# )
# print(message)



# Vision

# import anthropic
# import base64
# import httpx
#
# # Option 1: Base64-encoded image
# image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
# image_media_type = "image/jpeg"
# image_data = base64.standard_b64encode(httpx.get(image_url).content).decode("utf-8")
#
# message = anthropic.Anthropic().messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1024,
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "image",
#                     "source": {
#                         "type": "base64",
#                         "media_type": image_media_type,
#                         "data": image_data,
#                     },
#                 },
#                 {
#                     "type": "text",
#                     "text": "What is in the above image?"
#                 }
#             ],
#         }
#     ],
# )
# print(message)
#
# # Option 2: URL-referenced image
# message_from_url = anthropic.Anthropic().messages.create(
#     model="claude-sonnet-4-5",
#     max_tokens=1024,
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "image",
#                     "source": {
#                         "type": "url",
#                         "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
#                     },
#                 },
#                 {
#                     "type": "text",
#                     "text": "What is in the above image?"
#                 }
#             ],
#         }
#     ],
# )
# print(message_from_url)
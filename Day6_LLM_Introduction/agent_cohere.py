import os
import cohere

co = cohere.Client(os.getenv("COHERE_API_KEY")) # This is your trial API key

response = co.embed(
  model='embed-english-v3.0',
  texts=["tell me something about AI"],
  input_type='classification',
  truncate='NONE'
)

print('Embeddings: {}'.format(response.embeddings))
print('Response: {}',response)
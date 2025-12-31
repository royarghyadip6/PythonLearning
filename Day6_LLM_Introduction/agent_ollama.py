from ollama import chat

model="llama3.2:1b"
response = chat(
    model,
    messages=[
        {"role": "system", "content": "You are a helpful AI agent."},
        {"role": "user", "content": "Explain LLMs in one line"}
    ]
)

print(response["message"]["content"])
print(f'{"*"*50}')
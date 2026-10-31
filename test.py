from openai import OpenAI

# Initialize the client
client = OpenAI(api_key="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")

# Make a chat completion
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(response.choices[0].message.content)

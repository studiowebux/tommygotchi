from openai import OpenAI

client = OpenAI(api_key='None', base_url='http://localhost:8000/v1')


stream = client.chat.completions.create(
    model="llama-2-13b-chat",
    messages=[{"role": "user", "content": "Hello !"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

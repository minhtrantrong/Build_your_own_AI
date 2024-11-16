from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'user',
            'content': 'Who is the current Vietnam President?',
        }
    ],
    model='gemma2:2b',
)

print(chat_completion.choices[0].message.content)
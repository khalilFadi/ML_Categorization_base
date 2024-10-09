from openai import OpenAI
import os
# os.environ['OPENAI_API_KEY'] = "your_api_key_here"

import openai

# Set your actual API key here
# openai.api_key = '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'
client = OpenAI(api_key='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')
# client.api_key = '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'

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)
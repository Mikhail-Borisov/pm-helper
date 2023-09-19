import os
import openai

OPENAI_API_KEY = os.environ['OPENAI_API_KEY'].strip()
openai.api_key = OPENAI_API_KEY

def ask_chatgpt(prompt, model='gpt-3.5-turbo'):
    messages = [{'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message['content'] # type: ignore

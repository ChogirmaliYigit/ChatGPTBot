import openai
from data.config import OPENAI_KEY

openai.api_key = OPENAI_KEY

def chat_with_gpt(messages):
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7
    )
    return completion.choices[0].message['content']
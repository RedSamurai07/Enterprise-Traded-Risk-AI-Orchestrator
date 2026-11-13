import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPEN_API_KEY')
if not api_key:
    raise RuntimeError('Set the OPENROUTER_API_KEY environment variable to your OpenRouter API key.')
base_url = 'https://openrouter.ai/api/v1'

client = OpenAI(api_key=api_key, base_url=base_url)
model_name = 'nvidia/nemotron-3-ultra-550b-a55b:free'

response = client.chat.completions.create(
    model = model_name,
    messages = [
        {'role':'system','content':'You are a helpful assistant.'},
        {'role':'user','content':'Write a short poem about the beauty of nature.'}
    ],
    temperature = 0.6,
    max_tokens = 100,
    top_p = 1)
print(response.choices[0].message.content)
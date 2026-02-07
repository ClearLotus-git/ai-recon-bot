import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {"role": "user", "content": "Say hello from AI Recon Bot!"}
    ]
)

print(response.choices[0].message.content)

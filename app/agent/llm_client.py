import os
from openai import OpenAI
from dotenv import load_dotenv
import app.core.config as config

load_dotenv()

client = OpenAI(
    api_key=os.getenv(config.API_KEY_ENV_VAR),
    base_url=config.BASE_URL
)

def ask_llm(messages, max_tokens=256, temperature=0.0):
    prompt = "\n".join([m["content"] for m in messages])
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].message.content.strip() # type: ignore


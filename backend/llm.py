from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("api_key"))

def classify_message(text):

    prompt = f"""
    Classify this message:
    "{text}"

    Return JSON:
    {{
      "type": "friendly/normal/abusive",
      "score": 0 to 1
    }}
    """

    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )

    content = chat.choices[0].message.content

    try:
        return eval(content)
    except:
        return {"type": "normal", "score": 0.2}
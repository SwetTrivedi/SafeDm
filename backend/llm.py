# from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq(api_key=os.getenv("api_key"))

# def classify_message(text):

#     prompt = f"""
#     Classify this message:
#     "{text}"

#     Return JSON:
#     {{
#       "type": "friendly/normal/abusive",
#       "score": 0 to 1
#     }}
#     """

#     chat = client.chat.completions.create(
#         messages=[{"role": "user", "content": prompt}],
#         model="llama-3.1-8b-instant"
#     )

#     content = chat.choices[0].message.content

#     try:
#         return eval(content)
#     except:
#         return {"type": "normal", "score": 0.2}


from groq import Groq
import os
import json

# 🔐 env variables
client = Groq(api_key=os.getenv("api_key"))

bad_words_env = os.getenv("BAD_WORDS", "")
BAD_WORDS = bad_words_env.split(",")

def classify_message(text):

    text_lower = text.lower()

    # ⚡ STEP 1: quick keyword check
    for word in BAD_WORDS:
        if word and word in text_lower:
            return {"type": "abusive", "score": 0.6}

    # 🤖 STEP 2: AI check
    prompt = f"""
    Classify this message:
    "{text}"

    Return ONLY JSON:
    {{
      "type": "abusive/normal",
      "score": 0.0 to 1.0
    }}
    """

    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )

        content = chat.choices[0].message.content.strip()
        return json.loads(content)

    except Exception as e:
        print("ERROR:", e)
        return {"type": "normal", "score": 0.2}
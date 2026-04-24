# from fastapi import FastAPI
# from pydantic import BaseModel
# from backend.llm import classify_message

# app = FastAPI()

# class Msg(BaseModel):
#     msg: str
#     sender: str

# @app.post("/analyze")
# def analyze(data: Msg):

#     result = classify_message(data.msg)

#     score = result["score"]
#     msg_type = result["type"]

#     if msg_type == "abusive":
#         action = "block"
#     elif msg_type == "normal":
#         action = "allow"
#     else:
#         action = "warn"

#     return {
#         "action": action,
#         "score": score
#     }


from fastapi import FastAPI
from pydantic import BaseModel
from backend.llm import classify_message

app = FastAPI()

class Msg(BaseModel):
    msg: str
    sender: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/analyze")
def analyze(data: Msg):

    result = classify_message(data.msg)

    score = result.get("score", 0)
    msg_type = result.get("type", "normal")

    # 🎯 final decision
    if msg_type == "abusive" and score > 0.7:
        action = "block"

    elif msg_type == "abusive":
        action = "warn"

    else:
        action = "allow"

    return {
        "action": action,
        "score": score
    }
from fastapi import FastAPI
from pydantic import BaseModel
from llm import classify_message

app = FastAPI()

class Msg(BaseModel):
    msg: str
    sender: str

@app.post("/analyze")
def analyze(data: Msg):

    result = classify_message(data.msg)

    score = result["score"]
    msg_type = result["type"]

    if msg_type == "abusive":
        action = "block"
    elif msg_type == "normal":
        action = "allow"
    else:
        action = "warn"

    return {
        "action": action,
        "score": score
    }
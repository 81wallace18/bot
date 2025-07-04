from fastapi import FastAPI
from pydantic import BaseModel

from agent import handle_message

app = FastAPI()

class MessagePayload(BaseModel):
    user_id: str
    message: str

@app.post("/process-message")
async def process_message(payload: MessagePayload):
    response = handle_message(payload.user_id, payload.message)
    
    return response
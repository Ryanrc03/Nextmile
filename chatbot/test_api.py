from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    # Replace this with your chatbot logic
    response = {"reply": f"Echo: {message.text}"}
    return response
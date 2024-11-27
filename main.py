from fastapi import FastAPI
from api import chat

app = FastAPI()
app.include_router(chat.router, prefix="/api/chat")

@app.get("/")
async def root():
    return {"message": "Real time Bus Chat Service"}


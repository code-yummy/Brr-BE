from fastapi import FastAPI
from api import chat
from api.user_router import user_router
from api import bus_stop

app.include_router(chat.router, prefix="/api/chat")
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(bus_stop.router)

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

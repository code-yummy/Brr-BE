from fastapi import FastAPI

from api import bus_stop

app = FastAPI()
app.include_router(bus_stop.router)


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

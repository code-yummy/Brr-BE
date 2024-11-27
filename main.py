from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Real time Bus Chat Service"}
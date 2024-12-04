from fastapi import FastAPI
from api.user_router import user_router

app = FastAPI()

app.include_router(user_router, prefix="/api/users", tags=["Users"])

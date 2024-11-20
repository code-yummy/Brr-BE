from pydantic import BaseModel

class UserRequest(BaseModel):
    id: str | None = None
    password: str | None = None
    nickname: str | None = None

class PostRequest(BaseModel):
    title: str
    body: str
    userId: str
    password: str

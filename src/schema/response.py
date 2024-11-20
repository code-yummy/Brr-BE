from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    message: str

class PostResponse(BaseModel):
    title: str
    body: str
    writer: str
    written_at: str
    modifier: Optional[str] = None
    modified_at: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

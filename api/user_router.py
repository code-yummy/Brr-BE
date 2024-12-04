from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service.user import UserService
from utils.auth import create_access_token, decode_access_token


user_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


class UserRequest(BaseModel):
    email: str
    password: str
    nickname: Optional[str] = None


@user_router.post("/signup", status_code=201)
def signup(user_request: UserRequest):
    if user_service.sign_up(user_request.email, user_request.password, user_request.nickname):
        return {"message": "회원가입 성공"}
    raise HTTPException(status_code=400, detail="회원가입 실패")


@user_router.post("/login", status_code=200)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_email = form_data.username
    password = form_data.password
    if user_service.authenticate_user(user_email, password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="로그인 실패")


@user_router.get("/{email}", status_code=200)
def get_nickname(email: str, token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    if token_data.get("sub") != email:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    nickname = user_service.get_nickname(email)
    if nickname is None:
        raise HTTPException(status_code=404, detail="해당 회원이 존재하지 않습니다.")
    return {"nickname": nickname}


@user_router.put("/{email}/nickname", status_code=200)
def change_nickname(email: str, user_request: UserRequest, token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    if token_data.get("sub") != email:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    if user_service.change_nickname(email, user_request.password, user_request.nickname):
        return {"message": "닉네임 변경 성공"}
    raise HTTPException(status_code=400, detail="닉네임 변경 실패")


@user_router.put("/{email}/change-password", status_code=200)
def change_password(
    email: str, current_password: str, new_password: str, token: str = Depends(oauth2_scheme)
):
    token_data = decode_access_token(token)
    if token_data.get("sub") != email:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    if user_service.change_password(email, current_password, new_password):
        return {"message": "비밀번호 변경 성공"}
    raise HTTPException(status_code=400, detail="비밀번호 변경 실패")


@user_router.delete("/{email}", status_code=200)
def delete_user(email: str, user_request: UserRequest, token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    if token_data.get("sub") != email:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    if user_service.delete_user(email, user_request.password):
        return {"message": "회원 탈퇴 성공"}
    raise HTTPException(status_code=400, detail="회원 탈퇴 실패")

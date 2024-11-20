from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from post_service import PostService
from user_service import UserService
from user_repository import UserRepository
from post_repository import PostRepository

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

app = FastAPI()
user_repository = UserRepository()
post_repository = PostRepository()
user_service = UserService(user_repository)
post_service = PostService(post_repository)


class UserRequest(BaseModel):
    id: str | None = None
    password: str | None = None
    nickname: str | None = None


class PostRequest(BaseModel):
    title: str
    body: str
    userId: str
    password: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/api/users/signup", status_code=201)
def signup(user_request: UserRequest):
    if user_service.sign_up(user_request.id, user_request.password, user_request.nickname):
        return {"message": "회원가입 성공"}
    raise HTTPException(status_code=400, detail="회원가입 실패")


@app.post("/api/users/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_id = form_data.username
    password = form_data.password
    if user_service.authenticate_user(user_id, password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="로그인 실패")


@app.get("/api/users/{id}", status_code=200)
def get_nickname(id: str, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None or user_id != id:
            raise HTTPException(status_code=401, detail="권한이 없습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    nickname = user_service.get_nickname(id)
    if nickname is None:
        raise HTTPException(status_code=404, detail="해당 회원이 존재하지 않습니다.")
    return {"nickname": nickname}


@app.put("/api/users/{id}", status_code=200)
def change_nickname(id: str, user_request: UserRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None or user_id != id:
            raise HTTPException(status_code=401, detail="권한이 없습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    if user_service.change_nickname(user_id, user_request.password, user_request.nickname):
        return {"message": "닉네임 변경 성공"}
    raise HTTPException(status_code=400, detail="닉네임 변경 실패")


@app.delete("/api/users/{id}", status_code=200)
def delete_user(id: str, user_request: UserRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None or user_id != id:
            raise HTTPException(status_code=401, detail="권한이 없습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    if user_service.delete_user(user_id, user_request.password):
        return {"message": "회원 탈퇴 성공"}
    raise HTTPException(status_code=400, detail="회원 탈퇴 실패")


@app.post("/api/posts", status_code=201)
def publish_post(post_request: PostRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None or user_id != post_request.userId:
            raise HTTPException(status_code=401, detail="권한이 없습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    post_service.create_post(post_request.title, post_request.body, user_id)
    return {"message": "게시글 작성 성공"}


@app.get("/api/posts/{post_id}", status_code=200)
def get_post(post_id: int):
    post = post_service.read_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="게시글 조회 실패")
    response = {
        "title": post.title,
        "body": post.body,
        "writer": post.get_writer_nickname(),
        "written_at": post.written_at,
        "modifier": post.get_modifier_nickname(),
        "modified_at": post.modified_at
    }
    return response


@app.put("/api/posts/{post_id}", status_code=200)
def update_post(post_id: int, post_request: PostRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None or user_id != post_request.userId:
            raise HTTPException(status_code=401, detail="권한이 없습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    if not post_service.read_post(post_id) or not post_service.update_post(post_id, post_request.title, post_request.body, user_id):
        raise HTTPException(status_code=400, detail="게시글 수정 실패")
    return {"message": "게시글 수정 성공"}


@app.delete("/api/posts/{post_id}", status_code=200)
def delete_post(post_id: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")
    if not post_service.delete_post(post_id, user_id):
        raise HTTPException(status_code=400, detail="게시글 삭제 실패")
    return {"message": "게시글 삭제 성공"}

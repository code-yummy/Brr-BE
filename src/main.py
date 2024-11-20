from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str ="AI융합대학에서 시내로 가려고 합니다."

class ChatResponse(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Real time Bus Chat Service"}

def get_bus_info(message: str) -> str:
    print(f"Received message: {message}")  # 로그
    if "AI융합대학" in message and "시내" in message:
        return "5분 뒤에 출발해서 전남대 공과대학 정류장 OO버스를 타면 됩니다. 버스 도착 예정시간은 OO분 입니다."
    return "죄송합니다. 요청하신 정보를 처리할 수 없습니다."

@app.post("/api/chat",response_model=ChatResponse,status_code=200)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="입력값이 유효하지 않습니다.")
    response_message = get_bus_info(request.message)
    print(f"Response message: {response_message}") # 로그
    return {"message": response_message}

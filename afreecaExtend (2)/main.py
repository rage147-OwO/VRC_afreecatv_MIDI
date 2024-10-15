from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:8080",  # 허용할 클라이언트 도메인
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙을 위한 디렉터리 설정 (상위 디렉토리)
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# 각 화면에 해당하는 HTML 파일 엔드포인트
@app.get("/bj_screen.html")
async def bj_screen():
    return FileResponse("bj_screen.html")

@app.get("/mo_bj_screen.html")
async def mo_bj_screen():
    return FileResponse("mo_bj_screen.html")

@app.get("/user_screen.html")
async def user_screen():
    return FileResponse("user_screen.html")

@app.get("/mo_user_screen.html")
async def mo_user_screen():
    return FileResponse("mo_user_screen.html")

@app.get("/broadcast_screen.html")
async def broadcast_screen():
    return FileResponse("broadcast_screen.html")

@app.get("/mo_broadcast_screen.html")
async def mo_broadcast_screen():
    return FileResponse("mo_broadcast_screen.html")

# 사용자 정보를 제공하는 엔드포인트
@app.get("/get_user_info")
async def get_user_info():
    print("User info requested")
    user_info = {
        "username": "afreeca_user",  # 유저 이름
        "level": 10,                 # 유저 레벨
        "followers": 500             # 팔로워 수
    }
    return user_info

@app.get("/test")
async def user_info():
    print("User info requested")
    user_info = {
        "username": "afreeca_user",  # 유저 이름
        "level": 10,                 # 유저 레벨
        "followers": 500             # 팔로워 수
    }
    return user_info
\


# 메시지를 받는 엔드포인트
@app.post("/send_message")
async def send_message(message: dict):
    msg = message.get("message", "")
    print(f"Received message: {msg}")
    return {"status": "Message received", "message": msg}

# FastAPI 서버 실행 명령
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import mido
from mido import Message
import json



global port
app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:8000",  # 클라이언트 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/log")
async def log_message(log: dict):
    print("Received log:", log)  # 수신된 로그 출력

    # 로그 메시지에서 JSON 부분 추출
    try:
        log_content = log["log"].split("with: ")[1]  # 'with: ' 이후의 부분 가져오기
        log_data = json.loads(log_content)  # JSON으로 변환
    except (IndexError, json.JSONDecodeError):
        return JSONResponse(status_code=400, content={"error": "Invalid log format"})

    user_nickname = log_data.get("userNickname")  # userNickname 추출
    message = log_data.get("message")  # message 추출
    final = f"{user_nickname}: {message}"
    send_midi_message(final)

    return {"status": "Log received"}


    
# OPTIONS 요청을 처리하는 핸들러 추가
@app.options("/log")
async def options_log():
    return JSONResponse(content={"status": "CORS preflight successful"}, status_code=200)

import mido
from mido import Message
import time

signal_delay = 0.01  # 시그널 간격 (초)
def signal_send(channel, number, velocity):
    port.send(Message('note_on', note=number, velocity=velocity, channel=channel))
    time.sleep(signal_delay)  # Use the adjustable signal delay


def ushort_to_signal(value):
    channel = value >> 14
    number = (value >> 7) & 0x7F
    velocity = value & 0x7F
    signal_send(channel, number, velocity)




if __name__ == "__main__":

    # MIDI 출력 장치 선택
    #show midi devices
    device = "Springbeats vMIDI1 2"
    selected_output = [device for device in mido.get_output_names() if device.startswith("Springbeats")][0]
    port = mido.open_output(selected_output)
    #midi 기기 print
    

    message = "10"

    signal_send(3, 1, 1) #STX
    ushort_to_signal(int(message))
    signal_send(3, 1, 2) #ETX




    #import uvicorn
    #uvicorn.run(app, host="0.0.0.0", port=8000)




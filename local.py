#pyinstaller --onefile local.py --noconsole
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import mido
from mido import Message
import json
import os
import sys
import tkinter.messagebox as messagebox  # 메시지 박스를 추가
from tkinter import Tk, Label, Entry, Button, StringVar
import hashlib
import uuid
import time
import threading
import mido.backends.rtmidi

global port
app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:49152",  # 클라이언트 도메인
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
        log_content = log["log"].split("action received.")[1].strip()
        print(f"Log content extracted for JSON parsing: {log_content}")  # 디버깅용 출력

        # JSON으로 변환
        log_data = json.loads(log_content)

        # count 값을 추출
        count = log_data.get("count", None)
        if count is None:
            return JSONResponse(status_code=400, content={"error": "Count not found in log"})
        
        # 파싱하여 미디로 보내기
        signal_send(3, 1, 1)  # STX
        ushort_to_signal(int(count))
        signal_send(3, 1, 2)  # ETX
    except IndexError:
        return JSONResponse(status_code=400, content={"error": "Log format is incorrect. Missing action received."})
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"error": "Failed to decode JSON from log content."})

    return {"status": "Log received"}

# OPTIONS 요청을 처리하는 핸들러 추가
@app.options("/log")
async def options_log():
    return JSONResponse(content={"status": "CORS preflight successful"}, status_code=200)

signal_delay = 0.05  # 시그널 간격 (초)
def signal_send(channel, number, velocity):
    port.send(Message('note_on', note=number, velocity=velocity, channel=channel))
    time.sleep(signal_delay)  # Use the adjustable signal delay

def ushort_to_signal(value):
    channel = value >> 14
    number = (value >> 7) & 0x7F
    velocity = value & 0x7F
    signal_send(channel, number, velocity)

def get_mac_address():
    # MAC 주소를 얻기 위한 함수
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 8 * 6, 8)][::-1])
    return mac

def generate_serial(mac):
    # MAC 주소를 시드로 시리얼 생성
    sha = hashlib.sha256(mac.encode()).hexdigest()
    serial = sha[:12].upper()  # 시리얼의 일부분을 사용하여 표시 (12자)
    return serial

def verify_serial_key(serial, key):
    # 기대하는 시리얼에 맞는 키 생성 후 비교
    expected_key = generate_key_from_serial(serial)
    return key == expected_key

def generate_key_from_serial(serial):
    # 키 생성 로직 (외부 키 생성 프로그램과 동일해야 함)
    return hashlib.md5(serial.encode()).hexdigest()[:16].upper()

def open_midi_port():
    global port  # 전역 변수로 선언
    # MIDI 출력 장치 선택
    device = "Springbeats vMIDI1 2"
    selected_output = [device for device in mido.get_output_names() if device.startswith("Springbeats")]
    
    if selected_output:
        port = mido.open_output(selected_output[0])
        print("MIDI 포트가 성공적으로 열렸습니다:", selected_output[0])
    else:
        print("MIDI 출력 장치를 찾을 수 없습니다.")

def on_submit():
    entered_key = key_var.get()
    serial = serial_var.get()
    if verify_serial_key(serial, entered_key):
        print("인증 성공! 프로그램이 시작됩니다.")
        open_midi_port()  # 인증 성공 시 MIDI 포트를 엽니다.
        
        # 인증 성공 시 키 입력 부분 비활성화
        key_entry.config(state='disabled')
        serial_entry.config(state='disabled')
        
        # 작동 중 표시
        status_label.config(text="작동 중", fg="green")
        
        # 확인 버튼 비활성화
        submit_button.config(state='disabled')
    else:
        print("인증 실패! 올바른 키를 입력하세요.")

def on_exit():
    # 모든 프로세스를 종료
    print("프로그램이 종료됩니다.")
    if port:  # MIDI 포트가 열려 있다면 닫기
        port.close()
    root.quit()  # Tkinter 메인 루프 종료
    sys.exit()  # 프로그램 종료


def run_uvicorn():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=49152)

if __name__ == "__main__":
    # 현재 시스템의 MAC 주소 기반으로 시리얼 생성
    mac_address = get_mac_address()
    serial = generate_serial(mac_address)

    # 인증 UI 생성
    root = Tk()
    root.title("프로그램 인증")

    serial_var = StringVar(value=serial)
    key_var = StringVar()

    Label(root, text="시리얼:").grid(row=0, column=0)
    serial_entry = Entry(root, textvariable=serial_var, state='readonly')
    serial_entry.grid(row=0, column=1)

    Label(root, text="인증 키:").grid(row=1, column=0)
    key_entry = Entry(root, textvariable=key_var)
    key_entry.grid(row=1, column=1)

    # 작동 중 상태 라벨
    status_label = Label(root, text="")
    status_label.grid(row=3, column=0, columnspan=2)

    # 확인 버튼
    submit_button = Button(root, text="확인", command=on_submit)
    submit_button.grid(row=2, column=0, columnspan=2)

    # X 버튼 클릭 시 on_exit 호출
    root.protocol("WM_DELETE_WINDOW", on_exit)

    # Uvicorn을 별도의 스레드에서 실행
    threading.Thread(target=run_uvicorn, daemon=True).start()

    root.mainloop()

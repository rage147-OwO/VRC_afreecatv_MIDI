import hashlib
from tkinter import Tk, Label, Entry, Button, StringVar

def generate_key_from_serial(serial):
    # 인증 프로그램과 동일한 로직으로 키 생성
    return hashlib.md5(serial.encode()).hexdigest()[:16].upper()

def on_submit():
    serial_input = serial_var.get()
    key = generate_key_from_serial(serial_input)
    generated_key_var.set(key)

if __name__ == "__main__":
    # UI 생성
    root = Tk()
    root.title("키 생성기")

    serial_var = StringVar()
    generated_key_var = StringVar()

    Label(root, text="시리얼:").grid(row=0, column=0)
    Entry(root, textvariable=serial_var).grid(row=0, column=1)

    Button(root, text="키 생성", command=on_submit).grid(row=1, column=0, columnspan=2)

    Label(root, text="생성된 키:").grid(row=2, column=0)
    Entry(root, textvariable=generated_key_var, state='readonly').grid(row=2, column=1)

    root.mainloop()

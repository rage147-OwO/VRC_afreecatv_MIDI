import tkinter as tk
from tkinter import filedialog, ttk
import mido
from mido import Message
from PIL import Image, ExifTags
import time
import threading

# 전역 변수 및 이벤트 설정
stop_event = threading.Event()


def correct_image_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img._getexif()
        if exif is not None:
            orientation = exif.get(orientation, None)

            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # 이미지에 EXIF 데이터가 없을 때
        print("EXIF 데이터가 없습니다.")
        pass
    return img


def ushort_to_signal(value):
    channel = value >> 14
    number = (value >> 7) & 0x7F
    velocity = value & 0x7F
    signal_send(channel, number, velocity)

def signal_send(channel, number, velocity):
    port.send(Message('note_on', note=number, velocity=velocity, channel=channel))
    time.sleep(signal_delay)  # Use the adjustable signal delay

def send_image(image_path, size):
    with Image.open(image_path) as img:
        img = correct_image_orientation(img)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # 상하반전
        img = img.convert('RGB')
        # 이미지 크기 조정
        #0~10까지의 스케일로 이미지 크기 조정
        if size != 0:
            width, height = img.size
            img.thumbnail((width * size / 100, height * size / 100), Image.LANCZOS)

        width, height = img.size
        print(f"Image size: {width} x {height}")
    image_data = img.tobytes()
    total_bytes = len(image_data)
    print(f"Total bytes: {total_bytes}")

    signal_send(3, 1, 7)  # Init
    signal_send(3, 1, 3)  # Image width STX
    ushort_to_signal(width)
    signal_send(3, 1, 4)  # Image width ETX
    signal_send(3, 1, 5)  # Image height STX
    ushort_to_signal(height)
    signal_send(3, 1, 6)  # Image height ETX
    signal_send(3, 1, 1)  # Image data transmission STX
    
    for i in range(0, total_bytes, 2):
        if i + 1 < total_bytes:
            combined_bytes = (image_data[i] << 8) | image_data[i + 1]
        else:
            combined_bytes = image_data[i]
        ushort_to_signal(combined_bytes)

        progress = (i + 2) / total_bytes * 100
        progress_bar['value'] = progress  # Update progress bar
        root.update_idletasks()  # Update the UI

    signal_send(3, 1, 2)  # Send ETX after all data is transmitted
    progress_bar['value'] = 100  # Set progress to 100%

def threaded_send_image(image_path, size):
    stop_event.clear()  # 스레드 종료 요청 초기화
    progress_bar['value'] = 0  # Reset progress bar
    send_image(image_path, size)

thread = None
def select_image():
    # 진행 중인 스레드를 종료
    stop_event.set()  
    time.sleep(0.1)  # 약간의 지연을 추가하여 스레드 종료를 보장
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        scale_value = scale.get()
        threading.Thread(target=threaded_send_image, args=(file_path, scale_value)).start()

def update_delay(value):
    global signal_delay
    if value == "0":
        signal_delay = 0.1  # 느림 (안정)
    elif value == "1":
        signal_delay = 0.03  # 보통
    else:
        signal_delay = 0.0005  # 빠름 (불안정)

    delay_label_var.set(delay_labels[int(value)])  # Update label text

if __name__ == "__main__":
    signal_delay = 0.1  # Default delay in seconds
    delay_labels = ["느림(안정)", "보통", "빠름(불안정)"]
    
    device = "Springbeats vMIDI1 2"
    selected_output = [device for device in mido.get_output_names() if device.startswith("Springbeats")][0]
    port = mido.open_output(selected_output)

    root = tk.Tk()
    root.title("UdonLiveShare")
    root.geometry("400x400")  # Set a fixed window size
    root.configure(bg="#f0f0f0")

    # Add a frame for better organization
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(pady=20)

    label = tk.Label(main_frame, text="UdonLiveShare", font=("Helvetica", 16), bg="#f0f0f0")
    label.grid(row=0, columnspan=2, pady=10)

    tk.Label(main_frame, text="Size Scale (0-10):", bg="#f0f0f0").grid(row=1, columnspan=2)
    
    scale = tk.Scale(main_frame, from_=1, to=100, orient=tk.HORIZONTAL)
    scale.set(0)  # Default value
    scale.grid(row=2, columnspan=2, pady=10)

    select_button = tk.Button(main_frame, text="Select Image", command=select_image, bg="#0078d4", fg="white", padx=10, pady=5)
    select_button.grid(row=3, columnspan=2, pady=20)

    # Slider for signal delay
    delay_label_var = tk.StringVar(value=delay_labels[0])  # Default label
    delay_label = tk.Label(main_frame, textvariable=delay_label_var, bg="#f0f0f0")
    delay_label.grid(row=4, columnspan=2, pady=10)

    delay_slider = tk.Scale(main_frame, from_=0, to=2, orient=tk.HORIZONTAL, command=update_delay)
    delay_slider.set(0)  # Set default value to "느림(안정)"
    delay_slider.grid(row=5, columnspan=2, pady=10)

    progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
    progress_bar.grid(row=6, columnspan=2, pady=20)

    root.mainloop()

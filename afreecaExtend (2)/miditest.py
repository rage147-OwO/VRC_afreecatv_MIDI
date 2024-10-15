import mido
from mido import Message
import time


global port
def build_midi_char(char):
    #convert char to hex, max 
    hex_char = char.encode('utf-8').hex()
    #small endian
    hex_list = [int(hex_char[i:i+2], 16) for i in range(0, len(hex_char), 2)]
    port.send(Message('note_on', note=3, velocity=0))
    #sned length of hex_list
    port.send(Message('note_on', note=4, velocity=len(hex_list)))
    for i in range(len(hex_list)):
        #128보다 값이 크면
        if hex_list[i] > 128:
            port.send(Message('note_on', note=1, velocity= hex_list[i] - 128))
        else:
            port.send(Message('note_on', note=2, velocity=hex_list[i]))
    port.send(Message('note_on', note=5, velocity=0))
    #print all send hex


if __name__ == "__main__":
    # MIDI 출력 장치 선택
    #show midi devices
    device = "Springbeats vMIDI1 2"
    selected_output = [device for device in mido.get_output_names() if device.startswith("Springbeats")][0]
    port = mido.open_output(selected_output)
    #midi 기기 print
    text = '안녕하세요'
    build_midi_char(text)

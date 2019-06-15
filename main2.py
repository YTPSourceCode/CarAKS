import serial
import requests
import json
import time
import threading

def worker(end_point, data):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    try:
            r = requests.post('http://78.160.156.154:8000/api/{}/'.format(end_point), data=json.dumps(data), headers=headers)
    except:
        print("Data didnt send!")

bms = serial.Serial('/dev/tty.usbmodem1451',9600)
while 1:
    print(' ')
    row_data = bms.readline()
    clear_data = row_data.decode("utf-8")
    try:
        opcode = clear_data[:1]
        print(opcode)
    except:
        continue
    if opcode == 'i':
        if clear_data == None:
            continue
        try:
            isi = clear_data[2:]
            temperature_data = {"username": "car", "password": "yusufmerhaba", "engine_temperature":isi}
            temperature_thread = threading.Thread(target=worker, args=("temperature", temperature_data))
            temperature_thread.start()
        except:
            continue
        print('Isi').format(isi)
    if opcode == 'h':
        try:
            print(clear_data[1:])
            hiz = float(clear_data[1:])
            velocity_data = {"username": "car", "password": "yusufmerhaba", "velocity": hiz}
            velocity_thread = threading.Thread(target=worker, args=("velocity", velocity_data))
            velocity_thread.start()
        except:
            continue
        print('speed: {}'.format(hiz))

    time.sleep(0.2)

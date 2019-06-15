import serial
import requests
import json
import time
import threading

# Veri gönderimi için gereken thread
# server IP ve API end pointi burada
def worker(end_point, data):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        r = requests.post('http://85.98.189.145:8000/api/{}/'.format(end_point), data=json.dumps(data), headers=headers)
    except:
        print("Data didnt send!")

bms = serial.Serial('/dev/tty.usbserial',38400)
while 1:
    print(' ')
    row_data = bms.readline()
    clear_data = row_data.decode("utf-8")
    try:
        opcode = int(clear_data[6:8])
    except:
        continue
    if opcode <10:
        continue
    elif opcode == 26:
        try:
            minvolt = int(clear_data[13:17])/1000
            maxvolt = int(clear_data[18:22])/1000
            isi = float(clear_data[23:26])/10
            battery_voltage = float(((minvolt+maxvolt)/2)*20)
            battery = (battery_voltage - 56)*3.9

            #Burada worker fonksiyonu thread olarak cagrılıyor
            # JSON data burada oluşturuluyor
            ## !! ## REVIEW ## !!##
            # 1. Username ve password tekrar ediyor worker fonksiyonu içine gömülsün.
            voltage_data = {"username": "car", "password": "yusufmerhaba", "max_voltage": maxvolt,
                            "min_voltage": minvolt, "battery_voltage": battery}
            voltage_thread = threading.Thread(target=worker, args=("voltage", voltage_data))
            voltage_thread.start()

            # Isı için thread.
            ## !! ## REVIEW ## !!##
            # 1. Motor ısınının buraya çekilmesi gerekiyor. yada yeni endpoint lazım
            temperature_data = {"username": "car", "password": "yusufmerhaba",
                                "battery_temperature": isi, "engine_temperature": 0}
            temperature_thread = threading.Thread(target=worker, args=("temperature", temperature_data))
            temperature_thread.start()

        except:
            continue
        ## !! ## ERROR ## !!##
        # 1. '0' parametresini geçtigim degişken tanımlı degildi. degişkenin isminide unuttum duyrulur :)

        print('Max. Volt = {} \nMin. Volt = {}\nIsi = {}\nBatteryControl = {}\nBattery = {}'.format(maxvolt,minvolt,isi,0,battery))
    elif opcode == 24:
        try:
            current = int(clear_data[13:19])*10**-2
            # Akım için thread
            current_data = {"username": "car", "password": "yusufmerhaba", "current": current}
            current_thread = threading.Thread(target=worker, args=("current", current_data))
            current_thread.start()

            # Yusuf statusu apiye aktarmadım ama sor bizimkilere gerekiyorsa aktarayım.
            status = int(clear_data[20:21])
        except:
            continue
        print('current: {}\nBattery Status = {}'.format(current,status))


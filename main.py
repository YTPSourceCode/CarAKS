import serial

bms = serial.Serial('/dev/tty.usbserial',38400)

while 1:
    row_data = bms.readline()
    clear_data = row_data.decode("utf-8")
    try:
        opcode = int(clear_data[6:8])
    except:
        continue
    if opcode <10:
        continue
    if opcode == 26:
        try:
            minvolt = int(clear_data[13:17])/1000
            maxvolt = int(clear_data[18:22])/1000
            isi = float(clear_data[23:26])/10
            battery = float(((minvolt+maxvolt)/2)*20)*1.01
        except:
            continue
        if minvolt<3300:
            continue
        if maxvolt<3300:
            continue
        if isi>100:
            continue
        print('Max. Volt = {} \nMin. Volt = {}\nIsi = {}'.format(maxvolt,minvolt,isi))
        print('      ')
    if opcode == 24:
        try:
            current = int(clear_data[13:19])*10**-2
            status = int(clear_data[20:21])
        except:
            continue
        print('Current = {}'.format(current))

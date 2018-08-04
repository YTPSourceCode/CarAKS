import serial

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
        except:
            continue
        print('Max. Volt = {} \nMin. Volt = {}\nIsi = {}\nBatteryControl = {}\nBattery = {}'.format(maxvolt,minvolt,isi,battery_control,battery))
    elif opcode == 24:
        try:
            current = int(clear_data[13:19])*10**-2
            status = int(clear_data[20:21])
        except:
            continue
        print('current: {}\nBattery Status = {}'.format(current,status))

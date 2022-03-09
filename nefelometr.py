# Program do obsługi miernika GDM-9060 i nefelometru
#!/usr/bin/python3

import serial
import nfunc
from time import sleep
import atexit
import re

# SETTINGS
baud_meter = 115200
baud_ardu = 115200
com_meter = "/dev/ttyACM0" # win COM4
com_ardu = "/dev/ttyUSB0" # win COM7
timeout = 0
avg = True
mode = "conf:curr:dc 10e-4\n"


def doAtExit():
    meter.close()
    ardu.close()

if __name__ == "__main__":
    atexit.register(doAtExit)
    print("Oczekiwanie na połączenie z miernikiem")
    while(True):
        try:
            meter = serial.Serial(com_meter, baud_meter, timeout=timeout,
                                xonxoff=False, rtscts=False, dsrdtr=False)
            if(meter.is_open):
                break

        except Exception as e:
            print(e)
            com_meter = input("Wpisz właściwy port miernika: ")

    nfunc.ifprint(meter)

    while(True):
        try:
            ardu = serial.Serial(com_ardu, baud_ardu, timeout=timeout,
                                xonxoff=False, rtscts=False, dsrdtr=False)
            if(meter.is_open):
                break

        except Exception as e:
            print(e)
            com_ardu = input("Wpisz właściwy port arduino: ")
        # Waiting for aruino to connect

    ardu_msg = nfunc.rec_data(ardu)
    nfunc.ifprint(ardu_msg)
    if(not re.search("ArduReady", ardu_msg)):
        print("check arduino")


    # Meter setup for measuring current
    sleep(3)
    nfunc.send_cmd(meter, mode)

    print("Konfiguracja miernika:\n")
    nfunc.send_cmd(meter, "conf?\n")
    print(nfunc.rec_data(meter))
    sleep(1)

    print("Oczekiwanie na bazowanie")
    # waiting for arduino to home
    nfunc.send_cmd(ardu, "home.")
    while(True):
        if(not re.search("homed", nfunc.rec_data(ardu))):
            sleep(0.5)
        else:
            nfunc.send_cmd(ardu,"fwd:1")
            break
    print("Bazowanie zakończone")

    start_dist = int(input("odległość_początek: "))
    dist = int(input("odległość_koniec: "))
    step = int(input("krok: "))
    fname = input("nazwa pliku do zapisu: ")
    print("Pomiar rozpoczęty")
    nfunc.measure(meter, ardu, start_dist, dist, step, fname)


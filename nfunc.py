# Functions for automatic measuring

import re
from time import sleep

INFO_MODE = False    # Print more info to the user
AVG = 5 # Number of measuremets for counting average value
meter_command = "meas:curr:dc 10e-4?\n"

# Sending commands
def send_cmd(meter, msg):
    meter.write(msg.encode("ascii"))
    sleep(0.5) # time for receiving data

# Receiving data
def rec_data(device):
    while(device.inWaiting() == 0):
            sleep(0.1)
    return(device.readline().decode())
        
def ifprint(info):  # Print more info to the user
    if(INFO_MODE == True):
        print(info)
        
def prepareData(txt):
    stxt=re.sub("[^0-9,.Ee\-]", "", str(txt)) # Delete everything except values
    stxt=stxt.replace(',', ';')
    stxt=stxt.replace('.', ',')
    return(stxt)
        
def measure(device, ardu, start_dist, dist, step =1 , fname = "pomiar.txt"):
    global meter_command
    meas_data = []  # Variables for storing data saved in a file later
    dist_data = []
    
    send_cmd(ardu, "fwd:" + str(start_dist)) # Go to initial pos
    sleep(3);
    ifprint(rec_data(ardu))
    
    for i in range(int((dist-start_dist)/step)):
        dist_data.append(str(start_dist + i*step))
        
        #meter_msg = rec_data(device).rstrip()
        avg_val = []
        for j in range(AVG):
            send_cmd(device, meter_command)
            ifprint("waiting for meter")
            meter_msg = float(rec_data(device).rstrip())
            ifprint(meter_msg)
            avg_val.append(meter_msg)
            sleep(0.5)
        avg = str(sum(avg_val)/len(avg_val))
        meas_data.append(avg)
        print(str(dist_data[i]) + ": " + avg)
        
        sleep(2)
        
        send_cmd(ardu, "fwd:" + str(step))
        sleep(3);
        ifprint(rec_data(ardu))
        
    with open(fname, 'a') as f:
        data = prepareData(dist_data) + "\n" + prepareData(meas_data)
        f.write(data)
        
    print("Pomiar zakończony")

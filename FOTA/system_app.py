#!/usr/bin/python3
import threading
import os
import signal
from time import sleep
import RPi.GPIO as GPIO 
import hexSendBootloader


#start sequence and syncronization between RPI and STM

#System states
System_IDLE=0
Syetem_Initialize=1
System_Ready=2
System_Stop=3

#System state flage
start_stop_flage = System_IDLE

def process_Kill(name):
     
    try:
         
        # iterating through each instance of the process
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()
             
            # extracting Process ID from the output
            pid = fields[0]
             
            # terminating process
            os.kill(int(pid), signal.SIGKILL)
        print("Process Successfully terminated")
         
    except:
        print("Error Encountered while running script")

def System_Reset():
    while True :
        data_rec=ser.read()
        #if the responce from STM is No application 
        if data_rec.decode('utf-8') == 'n':
            print("system Need to flash")
            flash()

        #if the responce from STM is ready application 
        elif data_rec.decode('utf-8') == 'a':
            if start_stop_flage == 1:
                print("system start lidar")
                cmd = "./lidar --channel --serial /dev/ttyUSB0 115200 &"
                os.system(cmd)
                sleep(2)
                #request for STM to jump to the application
                ser.write('a'.encode('utf-8'))
            break



def System_Start():
    while True:
        if start_stop_flage == Syetem_Initialize:
            os.system("python3 firebase_Get_Update_Script.py &")
            ser.write('s'.encode('utf-8')) 
            print("system start")
            System_Reset()
            start_stop_flage = System_Ready
        sleep(1)



def System_Stop():
    while True:
        if start_stop_flage == System_Stop:
            file=open("/home/pi/Desktop/Update_Script/notify.txt","r")
            flage = file.read()
            file.close()
            #system kills lidar and fire base process
            process_Kill("lidar")
            process_Kill("firebase_Get_Update_Script")

            #system need to flash
            if flage == '1':
                print("system updating...")
                #Notify STM to be flashed
                ser.write('f'.encode('utf-8')) 
                System_Reset()
                file=open("/home/pi/Desktop/Update_Script/notify.txt","w")
                file.write("0")
                file.close()
            start_stop_flage = System_IDLE
        sleep(1)


def button_callback():
    if start_stop_flage == System_IDLE 
        start_stop_flage = Syetem_Initialize
    elif start_stop_flage == System_Ready:
        start_stop_flage = System_Stop



GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

t1 = threading.Thread(target=System_Start)
t2 = threading.Thread(target=System_Stop)
# starting thread 1
t1.start()
# starting thread 2
t2.start()
# wait until thread 1 is completely executed
t1.join()
# wait until thread 2 is completely executed
t2.join()



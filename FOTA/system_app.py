#!/usr/bin/python3
import threading
import os
import signal
from time import sleep
import subprocess
import RPi.GPIO as GPIO 
from hexSendBootloader import *


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
            os.kill(int(pid), signal.SIGINT)
        print("Process Successfully terminated")
         
    except:
        print("Error Encountered while running script")

def System_Reset():
    while True :
        global ser
        data_rec=ser.read(size=1)
        print(data_rec.decode('utf-8'))
        #if the responce from STM is No application 
        if data_rec.decode('utf-8') == 'n':
            print("system Need to flash")
            flash()
            file=open("/home/pi/ITI/FOTA/notify.txt","w")
            file.write("0")
            file.close()
            #flashing empty rom in STM
            if start_stop_flage == Syetem_Initialize :
                print("system start lidar")
                subprocess.Popen(["/home/pi/ITI/LIDAR/lidar --channel --serial /dev/ttyUSB0 115200"] , shell=True)
                sleep(2)
                #request for STM to jump to the application
                ser.write('j'.encode('utf-8'))

            #Updating the ROM in STM
            elif start_stop_flage == System_Stop:
                #request for STM to stop to the application
                ser.write('e'.encode('utf-8'))

            break

        #if the responce from STM is ready application 
        elif data_rec.decode('utf-8') == 'a':
            print("system start lidar")
            subprocess.Popen(["/home/pi/ITI/LIDAR/lidar --channel --serial /dev/ttyUSB0 115200"] , shell=True)
            sleep(2)
            #request for STM to jump to the application
            ser.write('j'.encode('utf-8'))
            break



def System_Start():
    global start_stop_flage, Syetem_Initialize,System_Ready, ser
    while True:
        if start_stop_flage == Syetem_Initialize:
            os.system("python3 firebase_Get_Update_Script.py &")
            ser.write('s'.encode('utf-8')) 
            print("system start")
            System_Reset()
            print("System_Ready")
            start_stop_flage = System_Ready
        sleep(0.5)



def System_Stop():
    global start_stop_flage, System_Stop, System_IDLE, ser
    while True:
        if start_stop_flage == System_Stop:
            file=open("/home/pi/ITI/FOTA/notify.txt","r")
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
                print("Flash done")
            start_stop_flage = System_IDLE

            else :
                #request for STM to stop to the application
                ser.write('e'.encode('utf-8'))
        sleep(0.5)


def button_callback(buffer):
    global start_stop_flage, System_IDLE, Syetem_Initialize, System_Ready, System_Stop
    if start_stop_flage == System_IDLE: 
        start_stop_flage = Syetem_Initialize
    elif start_stop_flage == System_Ready:
        start_stop_flage = System_Stop
    sleep(1)



GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(17,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge


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



import binascii
import time
import serial
import codecs
import re
from tqdm import tqdm
#Configurations for mini uart
PORT = '/dev/ttyS0'
BAUD_RATE = 9600

print ('opening serial port')


ser = serial.Serial(PORT, BAUD_RATE, timeout = None)
ser.reset_input_buffer()
ser.reset_output_buffer()

#Function name: flash()
#Function Desc:Send new hex file to STM32
def File_Len():
    lenth=0
    with open("Update.hex", "r") as file:
        for i in file:
            lenth = lenth+1
    return lenth

def flash():
    #open file
    with open("Update.hex", "r") as file:
        #looping on line line

        for i in tqdm(range(File_Len())):
            line = file.readline()
            for x in range(len(line)):
                if line[x] !='\n' and line[x] !='\r' :
                    ser.write(line[x].encode('utf-8'))
            ser.write('\r'.encode('utf-8'))  
            
            while True :
                data_rec=ser.read()
                #Waiting for micro controller to respond for continuing sending
                if data_rec.decode('utf-8') == 'o':
                    break
            #time.sleep(.01)
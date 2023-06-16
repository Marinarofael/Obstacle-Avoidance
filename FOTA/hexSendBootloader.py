import binascii
import time
import serial
import codecs
import re
#Configurations for mini uart
PORT = '/dev/ttyS0'
BAUD_RATE = 9600

print ('opening serial port')

#decomposing string of file to be sent character by character
string_pattern = b'.'
chunk = re.compile(string_pattern)

ser = serial.Serial(PORT, BAUD_RATE, timeout = None)
ser.flush()
#Function name: flash()
#Function Desc:Send new hex file to STM32
def flash():
    i = 1
    #open file
    with open("Update.hex", "rb") as file:
        #looping on line line
        for line in file:
            for l in line:
                   i+=1
                   #time.sleep(.05)
            result = chunk.findall(line)
            #sending Characters to STM32
            for x in range (len(result)):
                ser.write(result[x]) 
                #time.sleep(.01)
            ser.write('\n'.encode('utf-8'))     
            while True :
                data_rec=ser.read()
                #print(data_rec)
                #Waiting for micro controller to respond for continuing sending
                if data_rec.decode('utf-8') == 'o':
                    break
            #time.sleep(.01)

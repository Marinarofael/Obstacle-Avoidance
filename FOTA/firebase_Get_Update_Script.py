#!/usr/bin/python3

from time import sleep
import pyrebase


#===========================================================#
#	Opening version.txt File to Check on version number		#
#	Available now on STM32 Micro-controller					#
#===========================================================#


file_check=open("/home/pi/Desktop/Update_Script/version.txt","r")

version_check=int(file_check.read())

file_check.close()
#===========================================================#
#	A dictionary for cloud server project configuration		#
#===========================================================#
Config = {
  "apiKey": "AIzaSyDbI-O-xVXjs0QuQWo0MpcXZdYE4a8MmAs",
  "authDomain": "fota-ebe0a.firebaseapp.com",
  "databaseURL": "https://fota-ebe0a-default-rtdb.firebaseio.com",
  "projectId": "fota-ebe0a",
  "storageBucket": "fota-ebe0a.appspot.com",
  "serviceAccount": "/home/pi/Desktop/Update_Script/privatekey.json",
  "messagingSenderId": "1056175280604",
  "appId": "1:1056175280604:web:02f91b65ffe904abd0ff19",
  "measurementId": "G-QRVSKDM3E7"
}
#===================================================================#
#	Initializing cloud server project app and link it to python		#
#	Defining variable in which I saved firebse referrence in		#
#===================================================================#

firebase = pyrebase.initialize_app(Config)

#===================================================================#
#	A variable for cloud server project storage referrence			#
#===================================================================#

storage=firebase.storage()
#===================================================================#
#	A variable for referrence to project realtime database			#
#===================================================================#

database=firebase.database()

while True:
    current_version=database.child("version").get()
    

    if (version_check != current_version.val() ) :
	
        #A variable for cloud server project folders path#
        path_on_cloud="Files/Update.hex"
		#Downloading New update from Fire base Cloud#
        storage.child(path_on_cloud).download("/home/pi/Desktop/Update_Script/Update.hex")
        #Opening Text File to write new version #
		file=open("/home/pi/Desktop/Update_Script/version.txt","w")
        file.write(str(current_version.val()))
        file.close()
        version_check=current_version.val()
        exec (open("/home/pi/Desktop/Update_Script/GUI_Update_Notification.py").read())
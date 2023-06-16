#!/usr/bin/python3

from time import sleep
import pyrebase


#===========================================================#
#	Opening version.txt File to Check on version number		#
#	Available now on STM32 Micro-controller					#
#===========================================================#


file_check=open("/home/pi/ITI/FOTA/version.txt","r")

version_check=int(file_check.read())

file_check.close()
#===========================================================#
#	A dictionary for cloud server project configuration		#
#===========================================================#
Config = {
  "apiKey": "AIzaSyA4w08AuSqpJ86dxUZQE0krWcGk002tGb4",
  "authDomain": "fota-server-5e6af.firebaseapp.com",
  "databaseURL": "https://fota-server-5e6af-default-rtdb.firebaseio.com",
  "projectId": "fota-server-5e6af",
  "storageBucket": "fota-server-5e6af.appspot.com",
  "serviceAccount": "/home/pi/ITI/FOTA/privatekey.json",
  "messagingSenderId": "804173697125",
  "appId": "1:804173697125:web:6bfdb039e2ee66730b368c",
  "measurementId": "G-M1MN43F3SV"
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
	
        #A variable for cloud server project folders path
        path_on_cloud="Files/Update.hex"
		#Downloading New update from Fire base Cloud
        storage.child(path_on_cloud).download("/home/pi/ITI/FOTA/Update.hex")
        #Opening Text File to write new version
        file=open("/home/pi/ITI/FOTA/version.txt","w")
        file.write(str(current_version.val()))
        file.close()
        version_check=current_version.val()
        file=open("/home/pi/ITI/FOTA/notify.txt","w")
        file.write("1")
        file.close()
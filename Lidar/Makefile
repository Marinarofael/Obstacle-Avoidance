library_files = lib/lib_sdk.a
library_files += lib/wiringpi.a

source_files  = main.cpp


all:
	arm-linux-gnueabihf-g++ app/$(source_files) $(library_files) --static -I include/lidar_sdk -I include/wiringpi -o lidar
import serial
import time
import os
from datetime import datetime

file_period = 10
com = serial.Serial("COM11", timeout=0)

str_today = datetime.today().strftime("%y%m%d_%H%M_%S")
dir_name = "start_" + str_today
os.mkdir(dir_name)

str_today = datetime.today().strftime("%y%m%d_%H%M_%S")
file_name = "log_" + str_today
path_to_file_log = dir_name + '\\' + file_name + ".txt"
file_log = open(path_to_file_log, "wb") 

start = time.time()


while True:
	try:
		now = time.time()
		if now - start > file_period:
			file_log.close()
			str_today = datetime.today().strftime("%y%m%d_%H%M_%S")
			file_name = "log_" + str_today
			path_to_file_log = dir_name + '\\' + file_name + ".txt"
			file_log = open(path_to_file_log, "wb") 
			print("New file: {:s}".format(file_name))
			start = now

		rx_data = com.read()
		if rx_data != b'':
			file_log.write(rx_data)

	except KeyboardInterrupt:
		print("Received a keyboard interrupt!")
		break

if file_log.closed == False:
	file_log.close()

print()
print("End.")

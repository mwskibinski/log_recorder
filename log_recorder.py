from CONFIG import *
import serial
import time
import os
from datetime import datetime



# Convert current time to timestamp used to create names of files.
def get_filename_timestamp():
	return datetime.today().strftime("%y%m%d_%H%M_%S_%f")[:-3]

# Convert current time to timestamp printed in log (if set by flags in CONFIG).
def get_log_timestamp():
	return datetime.today().strftime("%y-%m-%d %H:%M:%S.%f")[:-3]

# Create new file to store logs.
def create_new_log_file():
	timestamp = get_filename_timestamp()
	file_name = "log_" + timestamp
	path_to_file_log = dir_name + '\\' + file_name + ".txt"
	file_log = open(path_to_file_log, "wb") 
	return file_log

# Create new file to store traces.
def create_new_trace_file():
	timestamp = get_filename_timestamp()
	file_name = "trace_" + timestamp
	path_to_file = dir_name + '\\' + file_name + ".bin"
	file = open(path_to_file, "wb") 
	return file

# Create directory where logs will be stored.
def create_dir_with_logs():
	timestamp = get_filename_timestamp()
	dir_name = "start_" + timestamp
	os.mkdir(dir_name)
	return dir_name

# Get string with transmitted command and current timestamp.
def get_cmd_string_with_timestamp(cmd):
	timestamp = get_log_timestamp()
	decoded_cmd = cmd.decode()
	cmd_string = "=== === now: {:s}".format(timestamp)
	cmd_string += ", tx cmd: {:s}".format(decoded_cmd)
	cmd_string += " === ===\r\n"
	return cmd_string

# Get string with transmitted command.
def get_cmd_string_without_timestamp(cmd):
	decoded_cmd = cmd.decode()
	cmd_string = "=== === tx cmd: {:s}".format(decoded_cmd)
	cmd_string += " === ===\r\n"
	return cmd_string

# Get command that will be printed next and its time interval.
def prepare_next_tx_cmd(tx_cmds, curr_idx):
	curr_idx = (curr_idx + 1) % len(tx_cmds)
	(cmd, interval) = get_current_tx_cmd(tx_cmds, curr_idx)
	return (curr_idx, cmd, interval)

# Get current command and time interval.
def get_current_tx_cmd(tx_cmds, curr_idx):
	cmd = tx_cmds[curr_idx]["cmd"]
	interval = tx_cmds[curr_idx]["interval"]
	return (cmd, interval)
	
# Get periodic timestamp that will be printed into log file
def get_periodic_timestamp():
	timestamp = get_log_timestamp()
	timestamp_line = "=== === now: {:s}".format(timestamp)
	timestamp_line += " === ===\r\n"
	return timestamp_line

# Get next position of cursor in trace file.
def get_curr_trace_addr(rx_line, trc_mark):
	trc_mark_idx = rx_line.find(trc_mark)
	addr_start_idx = trc_mark_idx + 6
	addr_end_idx = trc_mark_idx + 11
	addr = rx_line[addr_start_idx : addr_end_idx]
	addr = int(addr, 16)

	return (addr, addr_end_idx)

# Get data that will be stored in trace file.
def get_curr_trace_data(rx_line, addr_end_idx):
	data_start_idx = addr_end_idx + 2
	data_end_idx = rx_line.find(b'\r\n')
	data = rx_line[data_start_idx:data_end_idx]
	data = [
		int(data[i : i+2], 16).to_bytes(1, byteorder='big')
		for i in range(0, len(data), 2)
	]
	data_copy = data.copy()
	data = b''
	for d in data_copy: data += d

	return data

# Get current address and data to store them in trace file.
def get_trace_addr_and_data(rx_line, trc_mark):
	(addr, addr_end_idx) = get_curr_trace_addr(rx_line, trc_mark)
	data = get_curr_trace_data(rx_line, addr_end_idx)
	return (addr, data)

# Use to fill function reference with do-nothing functions.
def void_function(*pargs, **kwargs):
	pass



# Initialize reference to function that creates string to store at tx cmd event.
if print_cmd_at_tx == True and print_timestamp_at_tx == True:
	get_tx_string = get_cmd_string_with_timestamp
elif print_cmd_at_tx == True and print_timestamp_at_tx == False:
	get_tx_string = get_cmd_string_without_timestamp
elif print_cmd_at_tx == False and print_timestamp_at_tx == True:
	get_tx_string = get_periodic_timestamp
else:
	get_tx_string = void_function

# Initialize reference to function that gets periodic timestamps.
if print_timestamp_periodically_period != 0:
	get_tx_timestamp = get_periodic_timestamp
else:
	get_tx_timestamp = void_function

# Encode the commands. Leave intervals unchanged.
tx_cmds = [
	{ "cmd": tx_cmd["cmd"].encode(), "interval": tx_cmd["interval"] }
	for tx_cmd in tx_cmds
]

# Open chosen COM port.
com = serial.Serial(com_port, timeout=0)

# Create directory for logs.
dir_name = create_dir_with_logs()

# Create first file for this log session.
file_log = create_new_log_file()

# Initialize variables that store time of start of some operations.
file_start = time.time()
tx_start = time.time()
print_timestamp_start = time.time()

# Initialize remaining variables.
curr_tx_idx = 0 # Index used to get current command and its interval.
(curr_tx_cmd, curr_tx_interval) = get_current_tx_cmd(tx_cmds, curr_tx_idx)

timestamp_txt = None # String that holds timestamp that will be stored in the file.
tx_cmd_txt = None # String that holds transmitted command.
rx_buf = bytearray()
rx_line = None

# Trace consts.
trc_mark = "*~`trc".encode()
trc_init = trc_mark + ": INIT".encode()
trc_end = trc_mark + ": END".encode()

# Enter super loop.
while True:
	try:
		# Get current time.
		now = time.time()

		# Manage periodic operations.
		if now - file_start > file_lifetime:
			# Close current file and open a new one.
			file_log.close()
			file_log = create_new_log_file()
			file_start = now
		if now - tx_start > curr_tx_interval:
			# Send command. Get string to store in log file.
			com.write(curr_tx_cmd)
			tx_cmd_txt = get_tx_string(curr_tx_cmd)
			(curr_tx_idx, curr_tx_cmd, curr_tx_interval) = prepare_next_tx_cmd(tx_cmds, curr_tx_idx)
			tx_start = now
		if now - print_timestamp_start > print_timestamp_periodically_period:
			# Get periodic timestamp to be stored in log file.
			timestamp_txt = get_tx_timestamp()
			print_timestamp_start = now

		# Store current timestamp if timestamp line was created.
		if timestamp_txt != None:
			file_log.write(timestamp_txt.encode())
			timestamp_txt = None
		# Store transmitted command if such line was created.
		if tx_cmd_txt != None:
			file_log.write(tx_cmd_txt.encode())
			tx_cmd_txt = None
		# Store received data if line is ready.
		if rx_line != None:
			# If the line includes trace mark manage trace file.
			if trc_mark in rx_line:
				# If the line is trace-init line create trace file.
				if trc_init in rx_line:
					file_trc = create_new_trace_file()
				# If the line is trace-end line close the trace file.
				elif trc_end in rx_line:
					file_trc.close()
				# Otherwise store the received data as binary image.
				else:
					(addr, data) = get_trace_addr_and_data(rx_line, trc_mark)
					file_trc.seek(addr) # Potentially dangerous.
					file_trc.write(data)
			# Otherwise just store received line.
			else:
				file_log.write(rx_line)
			rx_line = None
				
		# Read data received from COM and create a line to store
		# if newline is somewhere in the line.
		rx_data = com.read()
		rx_buf.extend(rx_data)
		nl_idx = rx_buf.find(b'\n')
		if nl_idx != -1:
			rx_line = rx_buf[:nl_idx + 1]
			rx_buf = rx_buf[nl_idx + 2:]

	# Ctrl-C ends the whole thing.
	except KeyboardInterrupt:
		print("Received a keyboard interrupt!")
		break

# If keyboard interrupt occurred before the file was closed
# (which is more likely to happen) close it now.
if file_log.closed == False:
	file_log.close()

# Bye.
print()
print("End.")

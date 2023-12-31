import random
import time
import serial

max_len = 10
period = 500 * 1e-3
com = serial.Serial("COM10", timeout=0)

start = time.time()
rx_msg = bytearray()

while True:
	try:
		now = time.time()
		if now - start > period:
			lenn = (random.randbytes(1)[0] % max_len) + 1
			rand_bytes = [b % 26 for b in random.randbytes(lenn)]
			rand_nums = [ord('a') + num for num in rand_bytes]
			rand_txt = bytes(rand_nums).decode()
			tx_msg = "TX: " + rand_txt + "\r\n"
			print("msg: {:s}".format(tx_msg), end='')
			com.write(tx_msg.encode())
			start = now

		rx_data = com.read()	
		if rx_data != b'':
			rx_msg.extend(rx_data)
			rx_cmd = rx_msg.decode()
			if rx_cmd == "CTB A":
				tx_msg = "CTB A: !!!\r\n"
				print(tx_msg)
				com.write(bytes(tx_msg.encode()))
			elif rx_cmd == "CTB B":
				tx_msg = "CTB B: o1\r\n"
				print(tx_msg)
				com.write(bytes(tx_msg.encode()))
			
			if len(rx_cmd) == 5:
				print("clearing rx buf")
				rx_msg = bytearray()
			
	except KeyboardInterrupt:
		break

print()
print("End.")

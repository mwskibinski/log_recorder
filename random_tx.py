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
			tx_data = random.randbytes(lenn)
			com.write(tx_data)
			start = now
		rx_data = com.read()	
		if rx_data != b'':
			rx_msg.extend(rx_data)
			rx_cmd = rx_msg.decode()
			if rx_cmd == "CTB A":
				tx_msg = "CTB A: !!!"
				print(tx_msg)
				com.write(bytes(tx_msg.encode()))
			elif rx_cmd == "CTB B":
				tx_msg = "CTB B: o1"
				print(tx_msg)
				com.write(bytes(tx_msg.encode()))
			
			if len(rx_cmd) == 5:
				print("clearing rx buf")
				rx_msg = bytearray()
			
	except KeyboardInterrupt:
		break

print()
print("End.")

import serial
import time

max_len = 100
period = 1
com = serial.Serial("COM11", timeout=0)

start = time.time()

while True:
	try:
		now = time.time()
		if now - start > period:
			rx_data = com.read(max_len)
			if rx_data != b'':
				hex_str = ["{:02X}".format(b) for b in rx_data]
				print(" ".join(hex_str))
			start = now
	except KeyboardInterrupt:
		break

print()
print("End.")

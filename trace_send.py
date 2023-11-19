import random
import time
import serial

def rand_chance(success_prop_pcnt):
	randnum = int(random.randbytes(1)[0]) / 2.55
	result = True if randnum < success_prop_pcnt else False
	return result

max_len = 10
period = 500 * 1e-3
com = serial.Serial("COM10", timeout=0)

start = time.time()
rx_msg = bytearray()

trc_prefix = "*~`trc"
trc_addr = -1

while True:
	try:
		now = time.time()

		if now - start > period:
			if random.randbytes(1)[0] % 3 != 0:
				lenn = (random.randbytes(1)[0] % max_len) + 1
				rand_bytes = [b % 26 for b in random.randbytes(lenn)]
				rand_nums = [ord('a') + num for num in rand_bytes]
				rand_txt = bytes(rand_nums).decode()
				tx_msg = "TX: " + rand_txt + "\r\n"
				print("msg: {:s}".format(tx_msg), end='')
				com.write(tx_msg.encode())
				start = now
			else:
				if trc_addr == -1:
					tx_msg = trc_prefix + ": INIT" + "\r\n"
					trc_addr = 0
				elif trc_addr == -2:
					tx_msg = trc_prefix + ": END" + "\r\n"
					trc_addr = -1
				else:
					lenn = ((random.randbytes(1)[0] % max_len) + 1) * 2
					rand_bytes = [b % 16 for b in random.randbytes(lenn)]
					rand_nums = [
						ord('0') + num if num < 10
						else ord('a') + num - 10
						for num in rand_bytes
					]
					rand_txt = bytes(rand_nums).decode()
					tx_msg = trc_prefix + \
						"{:05x}: ".format(trc_addr) + rand_txt + "\r\n"
					trc_addr += lenn // 2
					if rand_chance(50): tr_addr += 1
					if trc_addr > 100:
						trc_addr = -2
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

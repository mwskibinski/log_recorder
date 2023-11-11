def hex_dump_a_file(path_to_file, max_row_len=50):
	file = open(path_to_file, "rb")
	max_bytes_read = (max_row_len - 11) // 3
	addr = 0
	while True:
		read_bytes = file.read(max_bytes_read)
		print("{:04X} {:04X}: ".format((addr & 0xFFFF_0000) >> 16, addr & 0x0000_FFFF), end='')
		addr += len(read_bytes)
		print_bytes_as_hex_dump(read_bytes)
		if len(read_bytes) != max_bytes_read:
			break
	file.close()

def print_bytes_as_hex_dump(byte_obj):
	print(bytes_into_hex_dump(byte_obj))

def bytes_into_hex_dump(byte_obj):
	hex_list = ["{:02X}".format(b) for b in byte_obj]
	txt = " ".join(hex_list)
	return txt

hex_dump_a_file('bytes_dummy.bin')

exit()

file = open("bytes.bin", "wb")
rx_line = "[asd][123123]*~`trc00000: 0123456789\r\n".encode()
trc_mark = "*~`trc".encode()

trc_mark_idx = rx_line.find(trc_mark)
addr_start_idx = trc_mark_idx + 6
addr_end_idx = trc_mark_idx + 11
addr = rx_line[addr_start_idx : addr_end_idx]
addr = int(addr, 16)
data_start_idx = addr_end_idx + 2
data_end_idx = rx_line.find(b'\r\n')
data = rx_line[data_start_idx:data_end_idx]
print(data)
data = [
	int(data[i : i+2], 16).to_bytes(1, byteorder='big')
	for i in range(0, len(data), 2)
]
data_copy = data.copy()
data = b''
for d in data_copy: data += d
print(data)
print_bytes_as_hex_dump(data)
exit()

file.write(data)

file.write(data)
file.close()

file = open("bytes.bin", "wb")
rx_line = "[asd][123123]*~`trc00000: 0123456789".encode()
trc_mark = "*~`trc"

trc_mark_idx = rx_line.find(trc_mark)
addr_start_idx = trc_mark_idx + 6
addr_end_idx = trc_mark_idx + 11
addr = rx_line[addr_start_idx : addr_end_idx]
addr = int(addr, 16)
data_start_idx = addr_end_idx + 2
data_end_idx = rx_line.find(b'\r\n')
data = rx_line[data_start_idx:data_end_idx]
data = [
int(data[i : i+2], 16).tobytes(1, byteorder='big')
for i in range(0, len(data), 2)
]
file_trc.write(data)

file.write(data)
file.close()

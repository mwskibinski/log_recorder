import os

"""
Hex dump a file.
"""
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

def print_option_string(option, description):
	print("\t{:s}\t{:s}")

def print_usage():
	print("USAGE:")
	print("\thexdump [options] <filename>")
	print("OPTIONS:")
	print_option_string("-cNUM", "Characters per row")
	print_option_string("-ANUM", "Maximum address")
	print_option_string("-aNUM", "Minimum address")
	print_option_string("-f", "Find")


"""
Start.
"""
def main():
	if len(os.sys.argv) <= 1:
		print_usage()
	else:
		for arg in os.sys.argv[1:]:
			if arg[0] == '-':
				flag = arg[1]
				match flag:
					case 'c':
						print('c')
					case _:
						print('DUPA')
			else:
				path = arg


def code1():
	path = None

	# -rNUM row len
	# -a print address
	# -sNUM separator for bytes NUM defualt 1
	# -Sx seprator character

	if len(os.sys.argv) <= 1:
		print_usage()
	else:
		for arg in os.sys.argv[1:]:
			if arg[0] == '-':
				flag = arg[1]
				match flag:
					case 'c':
						print('c')
					case _:
						print('DUPA')
			else:
				path = arg

def code2():
	from typing import Callable
	from dataclasses import dataclass

	@dataclass
	class Option:
		flag: str
		action: Callable
		description: str
	
	# o1 = Option(flag='c', action=None, description='update row size')
	# o1 = Option(flag='c', action=None, description='update row size', txt="abc")
	# o1 = Option('a', 'b', 'c')
	# o1 = Option('a', 'b', description='c')
	# o1 = Option('a', description='b', action='c')
	o1 = Option('a', description='b', action='c')

	print(o1)
	print(Option.__doc__)

def code3():
	o1 = dict(flag='c', action=None, description='abc')
	o1 = { "flag": 'c', "action": None, "description": 'abc' }
	o1 = { (1, 2, 3): 12 }
	# o1 = { [1, 2, 3]: 12 }

	# o1 = Option(flag='c', action=None, description='update row size', txt="abc")
	# o1 = Option('a', 'b', 'c')
	# o1 = Option('a', 'b', description='c')
	# o1 = Option('a', description='b', action='c')
	# o1 = Option('a', description='b', action='c')

	from typing import Callable

	print(o1)
	print(type(1))
	print(type(code3))
	print(type(abs))
	print(Callable[[int, int], tuple[str, str]])

main()

# TODO: Flags:
# - characters per row
# - range of addresses
# - separators: per how many bytes, what character
# - separators for address
# - find sequence of bytes
#
# - Create separate repo for this project
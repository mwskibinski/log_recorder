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
	print("\t{:s}\n\t\t{:s}".format(option, description))

def print_usage():
	print("USAGE:")
	print("\thexdump [options] <filename>")
	print("OPTIONS:")
	for opt in options:
		if opt["short_flag"] != None and opt["only_flag"] == False:
			left_str = "[-{:s} | --{:s}=] ARG".format(
				opt["short_flag"], opt["long_flag"])
		elif opt["short_flag"] != None and opt["only_flag"] == True:
			left_str = "[-{:s} | --{:s}]".format(
				opt["short_flag"], opt["long_flag"])
		elif opt["short_flag"] == None and opt["only_flag"] == False:
			left_str = "[--{:s}=] ARG".format(opt["long_flag"])
		elif opt["short_flag"] == None and opt["only_flag"] == True:
			left_str = "[--{:s}]".format(opt["long_flag"])

		print_option_string(left_str, opt["description"])


options = (
	dict(short_flag='c', long_flag='row_chars',
		occurred=False, action=None, only_flag=False,
		description="Characters per row"),
	dict(short_flag='M', long_flag='max_addr',
		occurred=False, action=None, only_flag=False,
		description="Maximum address"),
	dict(short_flag='m', long_flag='min_addr',
		occurred=False, action=None, only_flag=False,
		description="Minimum address"),
	dict(short_flag='b', long_flag='byte_sep_char',
		occurred=False, action=None, only_flag=False,
		description="Character used to seperate bytes of data"),
	dict(short_flag='B', long_flag='byte_sep_dist',
		occurred=False, action=None, only_flag=False,
		description="Number of data-bytes after which separator will occur"),
	dict(short_flag='a', long_flag='addr_sep_char',
		occurred=False, action=None, only_flag=False,
		description="Character used to seperate bytes of address"),
	dict(short_flag='A', long_flag='addr_sep_dist',
		occurred=False, action=None, only_flag=False,
		description="Number of bytes of address after which separator will occur"),
	dict(short_flag='p', long_flag='path',
		occurred=False, action=None, only_flag=False,
		description="Path to file which will be hex dumped"),
	dict(short_flag='v', long_flag='verbose',
		occurred=False, action=None, only_flag=True,
		description="Verbose"),
	dict(short_flag=None, long_flag='',
		occurred=False, action=None, only_flag=True,
		description="Used to indicate that no options will be provided next, only path"),
)

"""
Start.
"""
def main():
	if len(os.sys.argv) <= 1:
		print_usage()
	else:
		min_addr = 0
		max_addr = 0xFFFF_FFFF
		row_chars = 80
		byte_sep_char = ' '
		byte_sep_dist = 1
		addr_sep_char = ' '
		addr_sep_dist = 4
		path = ""
		verbose = False
	
		# TODO: Implement key-value pairs with spaces in between.

		for arg in os.sys.argv[1:]:
			if arg[0:2] == '--':
				key_end_idx = arg.find("=")
				key = arg[2:key_end_idx]
				val = arg[key_end_idx + 1 :]
				if verbose == True:
					print("long arg; key: {:s}, val: {:s}".format(key, val))
			elif arg[0] == '-':
				if len(arg) == 1:
					continue
				key = arg[1]
				val = arg[2 : ]
				if verbose == True:
					print("short arg; key: {:s}, val: {:s}".format(key, val))
			else:
				path = arg
				if verbose == True:
					print("path: {:s}".format(path))

		if verbose == True: print_config()
		start_hex_dump()


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
# - Flag-print even data which does not appear
# - Character used for N/A bytes
# - Verbose

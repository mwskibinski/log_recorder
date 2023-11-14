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

def update_key(val):
	return (False, None)

def get_number(val):
	result = False
	new_val = None
	if val[0:2] == "0x" or val[0:2] == "0X":
		new_val = int(val, 16)
	elif val[0:2] == "0b" or val[0:2] == "0B":
		new_val = int(val, 2)
	elif val[0:2] == "0o" or val[0:2] == "0O" or val[0] == '0':
		new_val = int(val, 8)
	else:
		new_val = int(val, 10)
	return (result, new_val)

def get_string(val):
	return (True, val)

def toggle_bool(key):
	(result, current) = get_option_value(key)
	new_val = not current
	return (result, new_val)

options = [
	dict(short_flag='c', long_flag='row_chars',
		occurred=False, action=get_number, only_flag=False, value=80,
		description="Characters per row"),
	dict(short_flag='M', long_flag='max_addr',
		occurred=False, action=get_number, only_flag=False, value=0xFFFF_FFFF,
		description="Maximum address"),
	dict(short_flag='m', long_flag='min_addr',
		occurred=False, action=get_number, only_flag=False, value=0x00,
		description="Minimum address"),
	dict(short_flag='b', long_flag='byte_sep_char',
		occurred=False, action=get_string, only_flag=False, value=' ',
		description="Character used to seperate bytes of data"),
	dict(short_flag='B', long_flag='byte_sep_dist',
		occurred=False, action=get_number, only_flag=False, value=1,
		description="Number of data-bytes after which separator will occur"),
	dict(short_flag='a', long_flag='addr_sep_char',
		occurred=False, action=get_string, only_flag=False, value=' ',
		description="Character used to seperate bytes of address"),
	dict(short_flag='A', long_flag='addr_sep_dist',
		occurred=False, action=get_number, only_flag=False, value=2,
		description="Number of bytes of address after which separator will occur"),
	dict(short_flag='p', long_flag='path',
		occurred=False, action=get_string, only_flag=False, value=None,
		description="Path to file which will be hex dumped"),
	dict(short_flag='v', long_flag='verbose',
		occurred=False, action=toggle_bool, only_flag=True, value=False,
		description="Verbose"),
	dict(short_flag=None, long_flag='',
		occurred=False, action=toggle_bool, only_flag=True, value=False,
		description="Used to indicate that no options will be provided next, only path"),
]

def get_option_value(name):
	result = None
	found = False
	for elem in options:
		if elem["long_flag"] == name:
			found = True
			result = elem["value"]
			break
	return (found, result)

def start_hex_dump():
	pass

def update_option(key, val, *, key_type):
	result = False
	update_idx = None
	flag_key = \
		"short_flag" if key_type == "short" else \
		"long_flag" if key_type == "long" else \
		None
	for idx, elem in enumerate(options):
		if elem[flag_key] == key:
			update_idx = idx
			break
	if update_idx != None:
		print(key, val, key_type, update_idx)
		if options[update_idx]["occurred"] == False:
			(result, new_val) = options[update_idx]["action"](val)
			if result == True:
				print(result, new_val)
				options[update_idx]["value"] = new_val
				options[update_idx]["occurred"] = True

	return result

def print_config():
	print("=== CONFIG:")
	for elem in options:
		print("name: {:15s}, val: {:15s}, occ: {:5s}".format(
			elem["long_flag"], str(elem["value"]), str(elem["occurred"])))
	print()



"""
Start.
"""
def main():
	if len(os.sys.argv) <= 1:
		print_usage()
	else:
		# TODO: Implement key-value pairs with spaces in between.
		for arg in os.sys.argv[1:]:
			if arg[0:2] == '--':
				key_end_idx = arg.find("=")
				if key_end_idx != -1:
					key = arg[2:key_end_idx]
					val = arg[key_end_idx + 1 :]
				else:
					key = arg[2:]
					val = ""
				if get_option_value("verbose")[1] == True:
					print("long arg; key: {:s}, val: {:s}".format(key, val))
				update_option(key, val, key_type="long")
			elif arg[0] == '-':
				if len(arg) == 1:
					continue
				key = arg[1]
				val = arg[2 : ]
				if get_option_value("verbose")[1] == True:
					print("short arg; key: {:s}, val: {:s}".format(key, val))
				update_option(key, val, key_type="short")
			else:
				val = arg
				key = "path"
				if get_option_value("verbose")[1] == True:
					print("path: {:s}".format(val))
				update_option(key, val, key_type="long")

		# if get_option_value("verbose")[1] == True: print_config()
		print_config()
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

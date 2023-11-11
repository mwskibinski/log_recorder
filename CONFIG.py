#
# Setup.
#

# Time variables are in unit of second.
# Use "* 1e-3" etc. to get millis.

# Time for which data will be stored in a single file.
# After the time elapses a new file will be created.
file_lifetime = 10

# Commands that will be sent to the card.
# Interval is a time that must pass from the last command transmission
# until the next command (i.e. cmd in the same row) will be transmitted.
# Add as many/little as you need.
tx_cmds = [
	{ "cmd": "CTB A", "interval": 1 },
	{ "cmd": "CTB B", "interval": 3 },
	{ "cmd": "CTB x", "interval": 4.5 },
]

# COM port used to communicate with logger.
com_port = "COM11"

# Print command when it is sent.
print_cmd_at_tx = False

# Print timestamp when command is sent.
print_timestamp_at_tx = False

# Print timestamp periodically.
# Set to 0 to disable.
print_timestamp_periodically_period = 0

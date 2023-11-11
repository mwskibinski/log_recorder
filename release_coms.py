from serial import Serial

try:
	com = Serial('COM10')
except:
	pass

try:
	com = Serial('COM11')
except:
	pass

import serial;

def filter(data):
	data_f = data.split(b' ')
	
	group = data_f[1]
	node = data_f[2]
	ct1 = [data_f[3], data_f[4]]
	ct2 = [data_f[5], data_f[6]]
	ct3 = [data_f[7], data_f[8]]
	ct4 = [data_f[9], data_f[10]]
	voltage = [data_f[11], data_f[12]]
	temp = [data_f[13], data_f[14]]

	current = (int(ct4[0]) + int(ct4[1]) * 256)/100.0
	voltage = (int(voltage[0]) + int(voltage[1]) * 256)/100.0
	temp = (int(temp[0]) + int(temp[1]) * 256)/10.0

	print('Current {0}A, Voltage {1}V, Temperature {2}C'.format(current, voltage, temp))

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0', 38400)
	print('Waiting data...')
	while True:
		data = ser.readline()
		if data[0:2] == b'OK':
			filter(data)

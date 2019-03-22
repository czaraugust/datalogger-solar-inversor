import serial;
import time;
import datetime

class Device:

	def __init__(self, ser):
		self.ser = ser
		self.last_second = 59
		self.raw_data = b''

		self.current_second = 0
		self.current = 0
		self.voltage = 0
		self.temperature = 0
		self.timestamp = 0

		self.csv_header = 'Hora|Corrente|Tensao|Temperatura\n'

	def _get_current_second(self):
		current_datetime = datetime.datetime.now()
		self.current_second = current_datetime.strftime('%S')
		self.timestamp = self._get_current_time()

	def _get_current_time(self):
		current_datetime = datetime.datetime.now()
		return current_datetime.strftime('%H:%M:%S')

	def _get_current_date(self):
		current_datetime = datetime.datetime.now()
		return current_datetime.strftime('%d%m%Y')

	def _format(self):
		data_f = self.raw_data.split(b' ')

        	group = data_f[1]
        	node = data_f[2]
        	ct1 = [data_f[3], data_f[4]]
        	ct2 = [data_f[5], data_f[6]]
        	ct3 = [data_f[7], data_f[8]]
        	ct4 = [data_f[9], data_f[10]]
        	voltage = [data_f[11], data_f[12]]
        	temp = [data_f[13], data_f[14]]

        	self.current = (int(ct4[0]) + int(ct4[1]) * 256)/100.0
        	self.voltage = (int(voltage[0]) + int(voltage[1]) * 256)/100.0
        	self.temperature = (int(temp[0]) + int(temp[1]) * 256)/10.0

	def sample(self):
		data = self.ser.readline()
		self._get_current_second()
		if self.current_second != self.last_second:
			if data[0:2] == b'OK':
				self.last_second = self.current_second
				self.raw_data = data
				self._format()
				print(self)
				self.save_to_file(self._get_current_time() == '00:00:00', str(self) + '\n')

	def __repr__(self):
		return 'Timestamp: {3}, Current {0}A, Voltage {1}V, Temperature {2}C'.format(self.current, self.voltage, self.temperature, self.timestamp)

	def __str__(self):
		return '{0}|{1}|{2}|{3}'.format(self.timestamp, self.current, self.voltage, self.temperature)

	def save_to_file(self, is_first, data):
		content = ''
		if is_first:
			content += self.csv_header
		content += data
		filename = self._get_current_date() + '.csv'
		with open(filename, 'a') as csv_file:
			csv_file.write(content)


if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyAMA0', 38400)
	dev = Device(ser)
	dev.save_to_file(True, '')
	print('Waiting data...')
	while True:
		dev.sample()

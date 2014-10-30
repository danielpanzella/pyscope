import circuits
from circuits.io import File, Serial
from circuits import Component, Event, Debugger, handler

class SensoDuino(Component):

	channel = "sensors"

	ID_ACCELEROMETER = "1"
	ID_MAGNETIC_FIELD = "2"
	ID_ORIENTATION = "3"
	ID_GYROSCOPE = "4"
	ID_LIGHT = "5"
	ID_PRESSURE = "6"
	ID_DEVICE_TEMPERATURE = "7"
	ID_PROXIMITY = "8"
	ID_GRAVITY = "9"
	ID_LINEAR_ACCELERATION = "10"
	ID_ROTATION_VECTOR = "11"
	ID_RELATIVE_HUMIDITY = "12"
	ID_AMBIENT_TEMPERATURE = "13"
	ID_MAGNETIC_FIELD_UNCALIBRATED = "14"
	ID_GAME_ROTATION_VECTOR = "15"
	ID_GYROSCOPE_UNCALIBRATED = "16"
	ID_SIGNIFICANT_MOTION = "17"
	ID_AUDIO = "97"
	ID_GPS1 = "98"
	ID_GPS2 = "99"

	def __init__ (self, source, isFile = False):
		super(SensoDuino, self).__init__()
		if isFile:
			self += File(source, channel=self.channel)
		else:
			self += Serial(source, channel=self.channel)

	def read(self, data):
		self.parse_data(data)

	def parse_data(self, csv_data):
		data = tuple(csv_data.strip('>\n').split(','))
		type_id = data[0]

		if type_id == self.ID_ACCELEROMETER:
			self.update_accelerometer(*data[2:5])
		elif type_id == self.ID_ORIENTATION:
			self.update_orientation(*data[2:5])
		elif type_id == self.ID_ROTATION_VECTOR:
			self.update_rotation_vector(*data[2:5])
		elif type_id == self.ID_MAGNETIC_FIELD:
			self.update_magnetic_field(*data[2:5])
		elif type_id == self.ID_GPS1:
			self.update_gps1(*data[2:5])
		elif type_id == self.ID_GPS2:
			self.update_gps2(*data[2:5])

	def update_accelerometer(self, x, y, z):
		self.fire(AccelerometerDataEvent((x, y, z)))#.notify = True
		return

	def update_orientation(self, yaw, pitch, roll):
		self.fire(OrientationDataEvent()).notify = True
		return

	def update_rotation_vector(self, x, y, z):
		self.fire(RotationVectorDataEvent()).notify = True
		return

	def update_magnetic_field(self, x, y, z):
		self.fire(MagneticFieldDataEvent()).notify = True
		return

	def update_gps1(self, latitude, longitude, altitude):
		self.fire(GPSDataEvent()).notify = True
		return

	def update_gps2(self, bearing, speed, datetime):
		self.fire(GPSDataEvent()).notify = True
		return


		
class SensorData(Event):
	"""SensorDataEvent"""

class AccelerometerDataEvent(SensorData):
	"""AccelerometerDataEvent"""

class OrientationDataEvent(SensorData):
	"""OrientationDataEvent"""

class GPSDataEvent(SensorData):
	"""GPSDataEvent"""

class RotationVectorDataEvent(SensorData):
	"""RotationVectorDataEvent"""

class MagneticFieldDataEvent(SensorData):
	"""MagneticFieldDataEvent"""

def main():
	(SensoDuino("/dev/cu.GalaxyNexus-SensoDuinoB") + Debugger()).run()

if __name__ == '__main__':
	main()
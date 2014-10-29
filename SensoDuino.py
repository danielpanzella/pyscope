import circuits
import circuits.io.serial
import circuits.io.file
from circuits import Component, Event

class SensoDuino(Component):
	CHANNEL_ALL = "all"
	CHANNEL_ACCELEROMETER = "accel"
	CHANNEL_MAGNETIC_FIELD = "mag_field"
	CHANNEL_ORIENTATION = "orient"
	CHANNEL_GYROSCOPE = "gyro"
	CHANNEL_LIGHT = "light"
	CHANNEL_PRESSURE = "pressure"
	CHANNEL_DEVICE_TEMPERATURE = "device_temp"
	CHANNEL_PROXIMITY = "prox"
	CHANNEL_GRAVITY = "grav"
	CHANNEL_LINEAR_ACCELERATION = "linear_accel"
	CHANNEL_ROTATION_VECTOR = "rot_vector"
	CHANNEL_RELATIVE_HUMIDITY = "rel_hum"
	CHANNEL_AMBIENT_TEMPERATURE = "amb_temp"
	CHANNEL_MAGNETIC_FIELD_UNCALIBRATED = "mag_field_uncal"
	CHANNEL_GAME_ROTATION_VECTOR = "game_rot_vector"
	CHANNEL_GYROSCOPE_UNCALIBRATED = "gyro_uncal"
	CHANNEL_SIGNIFICANT_MOTION = "sig_mot"
	CHANNEL_AUDIO = "audio"
	CHANNEL_GPS1 = "gps1"
	CHANNEL_GPS2 = "gps2"

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


	def __init__ (self, source, isFile = FALSE):
		super(SensoDuino, self).__init__()
		
	@handler("started	")
	def _on_start

	@handler("read")
	def on_read(self, data):
		return

	def parse_data(self, data):
		return


		
class SensorData(Event):
	"""SensorDataEvent"""

class AccelerometerDataEvent(SensorData)
	"""AccelerometerDataEvent"""

class OrientationDataEvent(SensorData):
	"""OrientationDataEvent"""

class GPSDataEvent(SensorData):
	"""GPSDataEvent"""

class RotationVectorDataEvent(SensorData):
	"""RotationVectorDataEvent"""

class MagneticFieldDataEvent(SensorData):
	"""MagneticFieldDataEvent"""

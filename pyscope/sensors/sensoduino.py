import circuits
from circuits.io import File, Serial
from circuits import Component, Debugger, handler, Timer
from circuits.node import Node, remote
from circuits.net.events import connect, ready
from .events import *

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

	def __init__ (self, source="dummy"):
		super(SensoDuino, self).__init__()
		self.event_data = {
			self.ID_ACCELEROMETER: {
				'event_type': AccelerometerDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
			self.ID_GRAVITY: {
				'event_type': GravityDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
			self.ID_ACCELEROMETER: {
				'event_type': AccelerometerDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
			self.ID_ORIENTATION: {
				'event_type': OrientationDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
			self.ID_ROTATION_VECTOR: {
				'event_type': RotationVectorDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
			self.ID_MAGNETIC_FIELD: {
				'event_type': MagneticFieldDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
			self.ID_GPS1: {
				'event_type': GPSDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
			self.ID_GPS2: {
				'event_type': GPSDataEvent,
				'last_event_data': { 'count': 0, "values": (0,0,0), "delta": (0,0,0) }
			},
		}
		if source != "dummy":
			self += Serial(source, baudrate=9600, timeout=10, channel=self.channel)
		else:
			event_data = self.event_data[self.ID_ACCELEROMETER]['last_event_data']
			Timer(
				1.0, 
				AccelerometerDataEvent(event_data['count'], event_data['values'], event_data['delta']), 
				(self.channel),
				persist=True
			).register(self)
	@handler("read")
	def _on_read(self, data):
		self._parse_data(data)

	def _parse_data(self, csv_data):
		data = tuple(csv_data.strip('>\n').split(','))
		type_id = data[0]
		current_event_count = data[1]
		current_values = tuple(float(datum) for datum in data[2:])

		previous_data = self.event_data[type_id]
		previous_event_count = previous_data['last_event_data']['count']
		previous_values = previous_data['last_event_data']['values']
		event_type = previous_data['event_type']

		if current_event_count <= previous_event_count:
			return

		delta_values = self.calc_delta(current_values, previous_values)
		previous_data['last_event_data']['count'] = current_event_count
		previous_data['last_event_data']['values'] = current_values
		previous_data['last_event_data']['delta'] = delta_values

		event = event_type(current_event_count, current_values, delta_values)
		self.fire(event)

	def calc_delta(self, current_values, previous_values):
		return tuple(
			curr - prev for curr, prev in zip(current_values, previous_values)
		)
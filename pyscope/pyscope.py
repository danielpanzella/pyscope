from .sensors.sensoduino import SensoDuino
from .remote.stellarium_server import StellariumServer, position_change
from .events import *
from circuits.io.events import close
from circuits import Component, Event, Debugger, handler
from pyrr import Quaternion, Matrix44, Vector3, quaternion
import numpy as np

class PyScope(Component):
	channel = 'pyscope'
	initial_direction = Vector3(0.0,1.0,0.0)

	def __init__(self, serial_port='/dev/cu.GalaxyNexus-SensoDuinoB'):
		super(PyScope, self).__init__()
		self.orientation = quaternion.create(0.0,0.0,0.0)
		self.direction = Vector3(0.0,1.0,0.0)
		self += SensoDuino(serial_port)
		self += StellariumServer()

	@handler('AccelerometerDataEvent', channel='sensors')
	def _update_accel(self, event_count, current_values, delta_values):
		print event_count
		print current_values
		print delta_values
		self._update_position()
		return

	@handler('RotationVectorDataEvent', channel='sensors')
	def _update_rotation(self, event_count, current_values, delta_values):
		self.orientation = quaternion.create(*current_values)
		self.direction = self.orientation * self.initial_direction
		self.fire(RotationVectorUpdated())
		return

	@handler('MagneticFieldDataEvent', channel='sensors')
	def _update_heading(self, event_count, current_values, delta_values):
		print event_count
		print current_values
		print delta_values
		self._update_position()
		return

	@handler("RotationVectorUpdated")
	def _update_coordinates(self)
		pass

	def _update_position(self):
		print self.direction
		self.fire(position_change(0, 0), 'stellarium')

	@handler('GPSDataEvent', channel='sensors')
	def update_location(self):
		self.fire(position_change(()), 'stellarium')
		return

	@handler('slew', channel='stellarium')
	def move_scope(self):
		return


def main():
	(PyScope() + Debugger()).run()

if __name__ == '__main__':
	main()
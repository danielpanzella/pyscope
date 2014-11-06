from circuits import Event

class SensorData(Event):
	'''SensorDataEvent'''

class AccelerometerDataEvent(SensorData):
	'''AccelerometerDataEvent'''

class GravityDataEvent(SensorData):
	'''GravityDataEvent'''

class OrientationDataEvent(SensorData):
	'''OrientationDataEvent'''

class GPSDataEvent(SensorData):
	'''GPSDataEvent'''

class RotationVectorDataEvent(SensorData):
	'''RotationVectorDataEvent'''

class MagneticFieldDataEvent(SensorData):
	'''MagneticFieldDataEvent'''
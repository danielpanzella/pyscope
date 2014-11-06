import serial

com = serial.Serial()
com.port = "/dev/cu.GalaxyNexus-SensoDuinoB"
com.timeout = 1
com.setDTR(False)
com.open()
com.close()
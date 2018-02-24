from math import degrees
from time import sleep
import RTIMU

SETTINGS_FILE = "/home/pi/Desktop/RTIMULib2/Linux/build/RTIMULibDemo/RTIMULib.ini"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
if (not imu.IMUInit()):
  print("IMU init failed")
  exit(1)
else:
  print("IMU init succeeded")
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
poll_interval = imu.IMUGetPollInterval()
cnt = 0

while True:
	if imu.IMURead():
		if cnt % 50 == 0:
			data = imu.getFusionData()
    			global roll, pitch, yaw
    			roll = degrees(data[0])
    			pitch = degrees(data[1])
    			yaw = degrees(data[2])
    			print(str(roll) + "   " + str(pitch) + "   " + str(yaw))
		cnt += 1

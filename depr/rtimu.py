from math import degrees
from time import sleep
import RTIMU


SETTINGS_FILE = "/home/pi/Desktop/RTIMULib2/Linux/build/RTIMULibDemo/RTIMULib.ini"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTPressure(s)
print(imu.pressureInit())
if (not imu.pressureInit()):
  print("IMU init failed")
  exit(1)
else:
  print("IMU init succeeded")
#imu.setSlerpPower(0.02)
#imu.setGyroEnable(True)
#imu.setAccelEnable(True)
#imu.setCompassEnable(True)
#poll_interval = imu.IMUGetPollInterval()
cnt = 0
offset_cnt = 0
offset_roll = 0
offset_pitch = 0
offset_yaw = 0

#Get offset values for roll pitch and yaw when program begins
#while offset_cnt <=10:
#	imu.pressureRead():
#		offset_data = imu.getFusionData()
#		offset_roll += (offset_data[0])
#      		offset_pitch += (offset_data[1])
#	       	offset_yaw += (offset_data[2])
#		offset_cnt +=1
#		sleep(0.2)

#offset_roll = degrees(offset_roll/offset_cnt)
#offset_pitch = degrees(offset_pitch/offset_cnt)
#offset_yaw = degrees(offset_yaw/offset_cnt)
#print("offset calculated")



while True:
#	if imu.IMURead():
	if cnt % 50 == 0:
		data = imu.pressureRead()
#		global roll, pitch, yaw
#		roll = degrees(data[0]) - (offset_roll)
#		pitch = degrees(data[1]) - (offset_pitch)
#		yaw = degrees(data[2]) - (offset_yaw)
		print(data)
		sleep(1)
	cnt += 1

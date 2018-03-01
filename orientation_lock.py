import cv2
import numpy as np
import pigpio
import RTIMU

from math import degrees
from time import sleep

def motor_init():
	global pi, SERVO_1, SERVO_2, init
	SERVO_1 = 12 #left motor
	SERVO_2 = 4 #right motor 
	SERVO_3 = 16 #
	SERVO_4 = 26 #

	pi = pigpio.pi()
	init = 1460

	print("init")
	pi.set_servo_pulsewidth(SERVO_1, init)
	pi.set_servo_pulsewidth(SERVO_2, init)
	pi.set_servo_pulsewidth(SERVO_3, init)
	pi.set_servo_pulsewidth(SERVO_4, init)

def orientation_correction(yaw):
	if -90 < yaw < -5:
		speed_left = 1515 + ((abs(yaw) - 5) * (1.5))
		speed_right = 1405 - ((abs(yaw) - 5) * (1.5))
		pi.set_servo_pulsewidth(SERVO_1, speed_left)
		pi.set_servo_pulsewidth(SERVO_2, speed_right)
		print(speed_left, speed_right)
	if 90 > yaw > 5:
		speed_left = 1405 - ((abs(yaw) - 5) * (1.5))
		speed_right = 1515 + ((abs(yaw) - 5) * (1.5))
		pi.set_servo_pulsewidth(SERVO_1, speed_left)
		pi.set_servo_pulsewidth(SERVO_2, speed_right)
		print(speed_left, speed_right)
	if -5 <= yaw <= 5:
		speed_left = init
		speed_right = init
		pi.set_servo_pulsewidth(SERVO_1, speed_left)
		pi.set_servo_pulsewidth(SERVO_2, speed_right)
		print(speed_left, speed_right)

motor_init()

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
offset_cnt = 0
offset_yaw = 0

#Get offset values for roll pitch and yaw when program begins
while offset_cnt <=10:
	if imu.IMURead():
		offset_data = imu.getFusionData()
	       	offset_yaw += (offset_data[2])
		offset_cnt +=1
		sleep(0.2)

offset_yaw = degrees(offset_yaw/offset_cnt)
print("offset calculated")

while True:
	if imu.IMURead():
		if cnt % 50 == 0:
			data = imu.getFusionData()
    			yaw = degrees(data[2]) - (offset_yaw)
    			print(str(yaw))
			orientation_correction(yaw)
		cnt += 1


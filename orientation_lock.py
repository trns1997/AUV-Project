import cv2
import numpy as np
import pigpio
import time

from rtimu import imu_init

def motor_init():
	global pi, SERVO_1, SERVO_2, init
	SERVO_1 = 26
	SERVO_2 = 16
	SERVO_3 = 4
	SERVO_4 = 12

	pi = pigpio.pi()
	init = 1460

	print("init")
	pi.set_servo_pulsewidth(SERVO_1, init)
	pi.set_servo_pulsewidth(SERVO_2, init)
	pi.set_servo_pulsewidth(SERVO_3, init)
	pi.set_servo_pulsewidth(SERVO_4, init)

def imu_init():
	global offset_roll, offset_pitch, offset_yaw, imu
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
	offset_roll = 0
	offset_pitch = 0
	offset_yaw = 0

	#Get offset values for roll pitch and yaw when program begins
	while offset_cnt <=10:
		if imu.IMURead():
			offset_data = imu.getFusionData()
			offset_roll += (offset_data[0])
	      		offset_pitch += (offset_data[1])
		       	offset_yaw += (offset_data[2])
			offset_cnt +=1
			sleep(0.2)

	offset_roll = degrees(offset_roll/offset_cnt)
	offset_pitch = degrees(offset_pitch/offset_cnt)
	offset_yaw = degrees(offset_yaw/offset_cnt)
	print("offset calculated")

def orientation_correction(yaw):
	if yaw < -5:
		speed_left = 1460 + abs(yaw)
		speed_right = 1460 - abs(yaw)
		pi.set_servo_pulsewidth(SERVO_1, speed_left)
		pi.set_servo_pulsewidth(SERVO_2, speed_right)
		print(speed_left, speed_right)
	if yaw > 5:
		speed_left = 1460 - abs(yaw)
		speed_right = 1460 + abs(yaw)
		pi.set_servo_pulsewidth(SERVO_1, speed_left)
		pi.set_servo_pulsewidth(SERVO_2, speed_right)
		print(speed_left, speed_right)

motor_init()
imu_init()

while True:
	if imu.IMURead():
		if cnt % 50 == 0:
			data = imu.getFusionData()
    			yaw = degrees(data[2]) - (offset_yaw)
    			print(str(yaw))
		cnt += 1


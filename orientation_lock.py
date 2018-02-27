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


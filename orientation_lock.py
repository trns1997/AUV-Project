import cv2
import numpy as np
import pigpio
import time

from optimizing import motor_init
from rtimu import imu_init

motor_init()
imu_init()

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

while True:
	if imu.IMURead():
		if cnt % 50 == 0:
			data = imu.getFusionData()
    			yaw = degrees(data[2]) - (offset_yaw)
    			print(str(yaw))
		cnt += 1


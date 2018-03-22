import cv2
import numpy as np
import pigpio
import RTIMU
import time
from math import degrees
from time import sleep

def motor_init():
	global pi, SERVO_1, SERVO_2, SERVO_3, SERVO_4, init
	SERVO_1 = 4 #left motor
	SERVO_2 = 12 #right motor
	SERVO_3 = 16 #
	SERVO_4 = 26 #

	pi = pigpio.pi()
	init = 1460

	print("init")
	pi.set_servo_pulsewidth(SERVO_1, init)
	pi.set_servo_pulsewidth(SERVO_2, init)
	pi.set_servo_pulsewidth(SERVO_3, init)
	pi.set_servo_pulsewidth(SERVO_4, init)

def orientation_correction(yaw, speed1, speed2):
        if -90 < yaw < -10:
                speed_right = 1515 + ((abs(yaw) - 10) * (1.5))
                speed_left = 1405 - ((abs(yaw) - 10) * (1.5))
                pi.set_servo_pulsewidth(SERVO_1, speed_left)
                pi.set_servo_pulsewidth(SERVO_2, speed_right)
                pi.set_servo_pulsewidth(SERVO_3, speed1)
                pi.set_servo_pulsewidth(SERVO_4, speed2)
#               print(speed_left, speed_right)
        if 90 > yaw > 10:
                speed_right = 1405 - ((abs(yaw) - 10) * (1.5))
                speed_left = 1515 + ((abs(yaw) - 10) * (1.5))
                pi.set_servo_pulsewidth(SERVO_1, speed_left)
                pi.set_servo_pulsewidth(SERVO_2, speed_right)
                pi.set_servo_pulsewidth(SERVO_3, speed1)
                pi.set_servo_pulsewidth(SERVO_4, speed2)
#               print(speed_left, speed_right)
        if -10 <= yaw <= 10:
                speed_left = 1380
                speed_right = 1380
                pi.set_servo_pulsewidth(SERVO_1, speed_left)
                pi.set_servo_pulsewidth(SERVO_2, speed_right)
                pi.set_servo_pulsewidth(SERVO_3, speed1)
                pi.set_servo_pulsewidth(SERVO_4, speed2)
#               print(speed_left, speed_right)


motor_init()

SETTINGS_FILE = "/home/pi/Desktop/RTIMULib2/Linux/build/RTIMULibDemo/RTIMULib.ini"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
#pres = RTIMU.RTPressure(s)
#print(pres.pressureInit())
if (not imu.IMUInit()):
  print("IMU init failed")
  exit(1)
else:
  print("IMU and Pressure init succeeded")
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

start_time = time.time()
while True:
	if(time.time() - start_time < 11):
		if imu.IMURead():
			if cnt % 50 == 0:
				data = imu.getFusionData()
    				yaw = degrees(data[2]) - (offset_yaw)
    				print(str(yaw))
				speed1 = 1200
				speed2 = 1600
				orientation_correction(yaw, speed1, speed2)
			cnt += 1
	elif (11 <= time.time() - start_time < 13):
		if imu.IMURead():
                        if cnt % 50 == 0:
                                data = imu.getFusionData()
                                yaw = degrees(data[2]) - (offset_yaw)
                                print(str(yaw))
				speed1 = 1600
				speed2 = 1200
                                orientation_correction(yaw, speed1, speed2)
			cnt += 1
	elif (13 <= time.time() - start_time < 16):
		if imu.IMURead():
                        if cnt % 50 == 0:
                                data = imu.getFusionData()
                                yaw = degrees(data[2]) - (offset_yaw)
                                print(str(yaw))
                                speed1 = init
                                speed2 = init
                                orientation_correction(yaw, speed1, speed2)
                        cnt += 1
	else:
		pi.set_servo_pulsewidth(SERVO_1, init)
                pi.set_servo_pulsewidth(SERVO_2, init)
                pi.set_servo_pulsewidth(SERVO_3, init)
                pi.set_servo_pulsewidth(SERVO_4, init)
		exit(1)



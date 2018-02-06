# import the necessary packages
import numpy as np
import turtle
import argparse
import cv2
import threading
from collections import deque
import imutils
#import serial
import struct

#ser = serial.Serial("COM3", 9600,)

rl = 0
gl = 0
bl = 0
ru = 0
gu = 0
bu = 0

def func():
	global rl,gl,bl,ru,gu,bu
	turtle.colormode(255)
	turtle.screensize(300,255)
	turtle.setworldcoordinates(0,0,300,255)

	red = turtle.Turtle()
	red.up()
	red.color("red")
	red.setx(0)

	green = turtle.Turtle()
	green.up()
	green.color("green")
	green.setx(60)

	blue = turtle.Turtle()
	blue.up()
	blue.color("blue")
	blue.setx(120)

	red1 = turtle.Turtle()
	red1.up()
	red1.color("red")
	red1.setx(180)

	green1 = turtle.Turtle()
	green1.up()
	green1.color("green")
	green1.setx(240)

	blue1 = turtle.Turtle()
	blue1.up()
	blue1.color("blue")
	blue1.setx(300)

	while (True):
		global rl,gl,bl,ru,gu,bu
		red.ondrag(red.goto)
		blue.ondrag(blue.goto)
		green.ondrag(green.goto)
		blue1.ondrag(blue1.goto)
		red1.ondrag(red1.goto)
		green1.ondrag(green1.goto)
		rl = int (red.ycor())
		gl = int (green.ycor())
		bl = int (blue.ycor())
		ru = int (red1.ycor())
		gu = int (green1.ycor())
		bu = int (blue1.ycor())
		turtle.bgcolor(ru,gu,bu)
		print(bl,gl,rl,bu,gu,ru)

	turtle.mainloop()
	
def cvfunc():
	while (True):
		# construct the argument parse and parse the arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-i", "--image", help = "path to the image")
		args = vars(ap.parse_args())
		# load the image
		image = cv2.imread(args["image"])
		#image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
		#image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
		# define the list of boundaries
		lower = (bl, gl, rl)
		upper = (bu, gu, ru)

		# loop over the boundaries
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)
			 
		# show the images
		image = imutils.resize(image, width=600)
		output = imutils.resize(output, width=600)

		cv2.imshow("poop", np.hstack([image, output]))
		cv2.waitKey(25)
		
def movfunc():
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	#ap.add_argument("-v", "--video",
	#	help="path to the (optional) video file")
	ap.add_argument("-i", "--image")
	ap.add_argument("-b", "--buffer", type=int, default=32,
		help="max buffer size")
	args = vars(ap.parse_args())

	# define the lower and upper boundaries of the "green"
	# ball in the HSV color space
	greenLower = (bl, gl, rl)
	greenUpper = (bu, gu, ru)
	 
	# initialize the list of tracked points, the frame counter,
	# and the coordinate deltas
	pts = deque(maxlen=args["buffer"])
	counter = 0
	(dX, dY) = (0, 0)
	direction = ""
	 
	# if a video path was not supplied, grab the reference
	# to the webcam
	if not args.get("video", False):
		camera = cv2.VideoCapture(0)
	 
	# otherwise, grab a reference to the video file
	else:
		camera = cv2.VideoCapture(args["video"])
		
	while True:
		# grab the current frame
		(grabbed, frame) = camera.read()
	 
		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		if args.get("video") and not grabbed:
			break
	 
		# resize the frame, blur it, and convert it to the HSV
		# color space
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	 
		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(frame, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
	 
		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			
			'''			
			if (x > 0 and x < 600) and (y > 0 and y < 600):
				a = 120 - (int(x/10))
				b = 110 - (int(y/10))
				ser.write(struct.pack('>BB',a,b))
				
			elif x > 600 or y > 60:
				a = 60
				b = 60
				ser.write(struct.pack('>BB',a,b))
			else:
				a = 0	
				b = 0
				ser.write(struct.pack('>BB',a,b))
				
			'''
	 
			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				pts.appendleft(center)

				
				# loop over the set of tracked points
			cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (0, 0, 255), 3)
			
			'''
			cv2.putText(frame, "dx: {}, dy: {}".format(a, b),
				(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.35, (0, 0, 255), 1)
			'''
	 
		# show the frame to our screen and increment the frame counter
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		counter += 1
	 
		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break
	 
	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()
	
t1 = threading.Thread(target = func)
t2 = threading.Thread(target = cvfunc)
#t3 = threading.Thread(target = movfunc)

t1.start()
t2.start()

#t1.join()

#t3.start()

#python detect_color.txt --image pink.png



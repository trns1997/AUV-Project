import numpy as np
import turtle
import argparse
import cv2
import threading
from collections import deque
import imutils
#import serial
import struct

def movfunc(rl,gl,bl,ru,gu,bu):

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

movfunc(36, 69, 13, 77, 248, 52)



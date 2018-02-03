import cv2
import numpy as np
import time

def viz(contours, median, color_flag):
	center = None
	point = []

	for i in range(len(contours)):
		# gets parameters for circles
		c = contours[i]
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
	# if statement to prevent contours that are too small to break program						
		if M["m00"] == 0:
			continue
		else:
			# computes centre
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))	
				# only proceed if the radius meets a minimum size
			if radius > 10 and color_flag == 0:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				#cv2.circle(img, (int(x), int(y)), int(radius),	
					#	(0, 255, 255), 2)
				# stores all the points in a array
				point.append(center)
				cv2.circle(median, center, 5, (0, 0, 255), -1)
				print("green")
			elif radius > 10 and color_flag == 1:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(img, (int(x), int(y)), int(radius),	
			#	(0, 255, 255), 2)
			# stores all the points in a array
				point.append(center)
				cv2.circle(median, center, 5, (0, 0, 255), -1)
				print("yellow")

	#cv2.imshow('mask',mask)
	cv2.imshow('Median Blur',median)


cap = cv2.VideoCapture(0)
frame_cnt = 0

lower_yellow = np.array([114, 145, 8])
upper_yellow = np.array([253, 246, 88])
lower_green = np.array([106, 11, 8])
upper_green = np.array([253, 136, 88])

list_color = [(lower_green, upper_green), (lower_yellow, upper_yellow)]

while(1):
	# Take each frame
	_, frame = cap.read()

	if frame_cnt % 20 == 0:
		#t0= time.clock()
		
		ycc = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

		mask1 = cv2.inRange(ycc, list_color[0][0], list_color[0][1])
		res1 = cv2.bitwise_and(frame,frame, mask= mask1)
		median1 = cv2.medianBlur(res1,15)

		mask2 = cv2.inRange(ycc, list_color[1][0], list_color[1][1])
		res2 = cv2.bitwise_and(frame,frame, mask= mask2)
		median2 = cv2.medianBlur(res2,15)

		contours1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
		contours2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
	
		if contours1 != []:
			viz(contours1, median1, 0)
		
		if contours2 != []:
			viz(contours2, median2, 1)
		
		#print(time.clock() - t0)
	
	frame_cnt = frame_cnt + 1

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()

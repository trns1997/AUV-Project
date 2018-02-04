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

		# if statement to prevent small contours to crash the program	
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
			elif radius > 10 and color_flag == 2:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				#cv2.circle(img, (int(x), int(y)), int(radius),	
				#	(0, 255, 255), 2)
				# stores all the points in a array
				point.append(center)
				cv2.circle(median, center, 5, (0, 0, 255), -1)
				print("pink")

	#cv2.imshow('mask',mask)
	cv2.imshow('Median Blur',median)


cap = cv2.VideoCapture(0)
frame_cnt = 0

lower_green = np.array([7, 8, 163])
upper_green = np.array([245, 113, 247])

lower_yellow = np.array([4, 140, 8])
upper_yellow = np.array([247, 248, 91])

lower_pink = np.array([6, 163, 6])
upper_pink = np.array([252, 250, 183])

list_color = [(lower_green, upper_green), (lower_yellow, upper_yellow), (lower_pink, upper_pink)]

while(1):
	# Take each frame
	_, frame = cap.read()

	if frame_cnt % 20 == 0:
		#t0= time.clock()
		biggest_contour_green = []
		biggest_contour_yellow = []
		biggest_contour_pink = []
		
		ycc = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
		lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

		mask_green = cv2.inRange(lab, list_color[0][0], list_color[0][1])

		mask_yellow = cv2.inRange(ycc, list_color[1][0], list_color[1][1])

		mask_pink = cv2.inRange(lab, list_color[2][0], list_color[2][1])

		contours_green = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
		
		contours_yellow = cv2.findContours(mask_yellow.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
		
		contours_pink = cv2.findContours(mask_pink.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]

		if len(contours_green) > 0:
			biggest_contour_green = max(contours_green, key=cv2.contourArea)
		
		if len(contours_yellow) > 0:
			biggest_contour_yellow = max(contours_yellow, key=cv2.contourArea)
			
		if len(contours_pink) > 0:
			biggest_contour_pink = max(contours_pink, key=cv2.contourArea)
		
		
		if len(biggest_contour_green) > len(biggest_contour_yellow) and len(biggest_contour_green) > len(biggest_contour_pink) :
			res_green = cv2.bitwise_and(frame,frame, mask= mask_green)
			median_green = cv2.medianBlur(res_green,15)
			viz(contours_green, median_green, 0)
		
		elif len(biggest_contour_yellow) > len(biggest_contour_green) and len(biggest_contour_yellow) > len(biggest_contour_pink):
			res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)
			median_yellow = cv2.medianBlur(res_yellow,15)
			viz(contours_yellow, median_yellow, 1)
		
		elif len(biggest_contour_pink) > len(biggest_contour_yellow) and len(biggest_contour_pink) > len(biggest_contour_green):
			res_pink = cv2.bitwise_and(frame,frame, mask= mask_pink)
			median_pink = cv2.medianBlur(res_pink,15)
			viz(contours_pink, median_pink, 2)
		
		#print(time.clock() - t0)
	
	frame_cnt = frame_cnt + 1

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()


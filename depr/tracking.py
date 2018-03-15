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
			
			# only proceeds if the radius meets a minimum size
			if radius > 10 and color_flag == 0:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				#cv2.circle(img, (int(x), int(y)), int(radius),	
					#	(0, 255, 255), 2)
				
				# stores all the points in a array
				point.append(center)
				cv2.circle(median, center, 5, (0, 0, 255), -1)
				#print("green")
				print(point)
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
	cv2.imshow('Result', median)


cap = cv2.VideoCapture(0)
frame_cnt = 0

# Define the lower and upper bounds range for a color in desired format(bgr/hsv/ycc/lab)
lower_green = np.array([73, 8, 9])
upper_green = np.array([252, 132, 100])

lower_yellow = np.array([10, 123, 5])
upper_yellow = np.array([252, 252, 75])

lower_pink = np.array([4, 185, 3])
upper_pink = np.array([252, 252, 252])

while(1):
	# Take each frame
	_, frame = cap.read()

	# Every 6th frame is processed
	if frame_cnt % 6 == 0:
		
		biggest_contour_green = []
		biggest_contour_yellow = []
		biggest_contour_pink = []
				
		frame = cv2.resize(frame, (500, 350)) 
		
		ycc = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

		mask_green = cv2.inRange(ycc, lower_green, upper_green)

		mask_yellow = cv2.inRange(ycc, lower_yellow, upper_yellow)

		mask_pink = cv2.inRange(ycc, lower_pink, upper_pink)

		contours_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
		
		contours_yellow = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
		
		contours_pink = cv2.findContours(mask_pink, cv2.RETR_EXTERNAL,
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
			viz(contours_green, res_green, 0)
		
		elif len(biggest_contour_yellow) > len(biggest_contour_green) and len(biggest_contour_yellow) > len(biggest_contour_pink):
			res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)
			median_yellow = cv2.medianBlur(res_yellow,15)
			viz(contours_yellow, res_yellow, 1)
		
		elif len(biggest_contour_pink) > len(biggest_contour_yellow) and len(biggest_contour_pink) > len(biggest_contour_green):
			res_pink = cv2.bitwise_and(frame,frame, mask= mask_pink)
			median_pink = cv2.medianBlur(res_pink,15)
			viz(contours_pink, res_pink, 2)
	
	frame_cnt = frame_cnt + 1

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()


import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cnt = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if cnt % 20 == 0:	
    # Our operations on the frame come here
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

    	# Display the resulting frame
    	cv2.imshow('frame',gray)
    cv2.imshow('e',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        	break
    cnt = cnt + 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

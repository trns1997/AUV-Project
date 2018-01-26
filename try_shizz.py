import numpy as np
import turtle
import argparse
import cv2
import threading
from collections import deque
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
# load the image
rgb = cv2.imread(args["image"])
rgb = imutils.resize(rgb, width=600)
lab = cv2.cvtColor(rgb, cv2.COLOR_BGR2LAB)
hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
ycc = cv2.cvtColor(rgb, cv2.COLOR_BGR2YCR_CB)

cv2.imshow("rgb", rgb)
cv2.imshow("lab", lab)
cv2.imshow("hsv", hsv)
cv2.imshow("ycc", ycc)
cv2.waitKey(0)

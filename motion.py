#!/usr/bin/env python2
 
"""
OpenCV example. Show webcam image and detect face.
"""
 
import cv2
import numpy as np

webcam = cv2.VideoCapture(2)
cv2.namedWindow("preview")
 
if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
else:
    rval = False
    import sys
    sys.exit(-1)
 
CENTER = (320, 260)
THRESH_PCT = 0.5

mask = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
    
cv2.circle(
  mask, 
  CENTER, 
  200, 
  255, 
  1
)
#cv2.floodFill(gray, mask, (20, 20), 255, 1, 1) #diff = np.subtract(dif, e)
avg = np.float32(mask)

exposure_level = 0

while rval:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.pyrDown(gray, gray)

    #blur = cv2.blur(gray, (30, 30))

    cv2.accumulateWeighted(gray,avg,0.1)
    favg = cv2.convertScaleAbs(avg)
    
    diff = gray - favg + 128

    # threshold out positive values or small negative ones
    (_, thr) = cv2.threshold(diff, 128 - 20, 255, cv2.THRESH_BINARY_INV)

    # detect faces and draw bounding boxes
    cv2.imshow("preview", thr)
 
    #maxval = np.amax(masked)
    #print maxval
    #thresh = maxval * THRESH_PCT

    #(_, thresholded) = cv2.threshold(masked, thresh, 255, cv2.THRESH_BINARY_INV)
    #thresholded = cv2.bitwise_and(thresholded, mask)
    #cv2.imshow("p2", thresholded)


    # get next frame
    rval, frame = webcam.read()

    key = cv2.waitKey(20)
    if key in [27, ord('Q'), ord('q')]: # exit on ESC
        break

#!/usr/bin/env python2
 
"""
OpenCV example. Show webcam image and detect face.
"""
 
import cv2
import numpy as np
import serial

webcam = cv2.VideoCapture(1)
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

ser = serial.Serial("/dev/ttyUSB0", 9600)

xr = [1024, 0]
yr = [1024, 0] # min, max

while rval:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #norm = cv2.equalizeHist(gray)
    cv2.pyrDown(gray, gray) # Downsample by half

    #cv2.imshow("gray", gray)
    cv2.accumulateWeighted(gray,avg,0.05)
    favg = cv2.convertScaleAbs(avg) # Get average image
    
    meancol = cv2.mean(favg) # TODO: Mask

    diff = gray - favg + 128

    # threshold out positive values or small negative ones
    (_, thr) = cv2.threshold(diff, meancol[0]+30, 255, cv2.THRESH_BINARY)

    # detect faces and draw bounding boxes
    #cv2.imshow("thresh", thr)
    
    kern = np.ones((3,3), np.uint8)
    thr = cv2.erode(thr, kernel=kern, iterations=5)
    thr = cv2.dilate(thr, kernel=kern,iterations=5)

    contours,hierarchy = cv2.findContours(thr,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(thr,(cx,cy),5,255,-1)

    if cx < xr[0]:
      xr[0] = cx - 1
    elif cx > xr[1]:
      xr[1] = cx

    if cy < yr[0]:
      yr[0] = cy - 1
    elif cy > yr[1]:
      yr[1] = cy

    cx = 255*(cx - xr[0])/(xr[1]-xr[0])
    cy = 255*(cy - yr[0])/(yr[1]-yr[0])
    print cx, cy
    ser.write("%d %d\n" % (cx, cy))

    # Show it, if key pessed is 'Esc', exit the loop
    cv2.imshow('frame', thr)

   # get next frame
    rval, frame = webcam.read()

    key = cv2.waitKey(20)
    if key in [27, ord('Q'), ord('q')]: # exit on ESC
        break

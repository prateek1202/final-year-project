import cv2
import numpy as np

frame_width = 640
frame_height = 480

cap = cv2.VideoCapture(1)
cap.set(3,frame_width)
cap.set(4,frame_height)

def empty(e):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,340)
cv2.createTrackbar("Hue Min", "HSV", 0,179,empty)
cv2.createTrackbar("Hue Max", "HSV", 179,179,empty)
cv2.createTrackbar("Sat Min", "HSV", 0,255,empty)
cv2.createTrackbar("Sat Max", "HSV", 255,255,empty)
cv2.createTrackbar("Value Min", "HSV", 0,255,empty)
cv2.createTrackbar("Value Max", "HSV", 255,255,empty)

cap = cv2.VideoCapture('http://192.168.29.202:4747/video')
frame_counter = 0

while True:
    frame_counter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
        cap.set(cv2.CAP_PROP_POS_FRAME,0)
        frame_counter = 0
        
    _,img = cap.read()
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    h_min = cv2.getTrackbarPos("Hue Min","HSV")
    h_max = cv2.getTrackbarPos("Hue Max","HSV")
    s_min = cv2.getTrackbarPos("Sat Min","HSV")
    s_max = cv2.getTrackbarPos("Sat Max","HSV")
    v_min = cv2.getTrackbarPos("Value Min","HSV")
    v_max = cv2.getTrackbarPos("Value Min","HSV")
    v_max = cv2.getTrackbarPos("Value Max","HSV")
    print(h_min)
    
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(img_hsv,lower,upper)
    result = cv2.bitwise_and(img,img,mask=mask)
    
    mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    h_stack = np.hstack([img,mask,result])
    cv2.imshow('Horizontal Stacking',h_stack)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        cv2.waitKey(0)
        
cap.release()
cv2.destoryAllWindows()
    
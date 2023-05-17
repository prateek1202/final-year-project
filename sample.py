import cv2
import utils
import numpy as np

# cap = cv2.VideoCapture('http://192.168.29.202:4747/video')
# while True:
#     succces,img = cap.read()
#     img = cv2.resize(img,(480,240))
#     img_thresh = utils.thresholding(img)
#     cv2.imshow("vid",img)
#     cv2.imshow("vid",img_thresh)
#     cv2.waitKey(1)

img = cv2.imread('image.jpeg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("image",img)

# define range of blue color in HSV
lower_yellow = np.array([15,50,180])
upper_yellow = np.array([40,255,255])
# Create a mask. Threshold the HSV image to get only yellow colors
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Bitwise-AND mask and original image
# result = cv2.bitwise_and(img,img, mask= mask)

# display the mask and masked image
cv2.imshow('Mask',mask)
cv2.waitKey(0)
# cv2.imshow('Masked Image',result)
cv2.waitKey(0)
cv2.destroyAllWindows()
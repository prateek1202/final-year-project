import cv2 as cv
stream = cv.VideoCapture("http://192.168.43.14:4747/video")

while True:
    r,f = stream.read()
    print(r,f)
    cv.imshow("IP camera",f)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.DestroyAllWindows()  
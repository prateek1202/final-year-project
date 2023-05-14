import cv2
import numpy as np

def thresholding(img):
    img_Hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_white = np.array([80,0,0])
    upper_white = np.array([255,160,255])
    mask_white = cv2.inRange(img_Hsv,lower_white,upper_white)
    
    return mask_white

def wrap_image(img,points,w,h,inv = False):
    points_1 = np.float32(points)
    points_2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    if inv:
        trans_matrix = cv2.getPerspectiveTransform(points_2,points_1)
    else:
        trans_matrix = cv2.getPerspectiveTransform(points_1,points_2)
    imgWarp = cv2.warpPerspective(img,trans_matrix,(w,h))
    return imgWarp

def nothing(a):
    pass

def initialize_trackbars(initial_tracebar_vals,wt = 480, ht = 240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars",360,240)
    cv2.createTrackbar("Width Top","Trackbars",int(initial_tracebar_vals[0]),int(wt/2),nothing)
    cv2.createTrackbar("Height Top","Trackbars",initial_tracebar_vals[1],ht,nothing)
    cv2.createTrackbar("Width Bottom","Trackbars",int(initial_tracebar_vals[2]),int(wt/2),nothing)
    cv2.createTrackbar("Height Bottom","Trackbars",initial_tracebar_vals[3],ht,nothing)
    
def val_trackbars(wt = 480,ht=480):
    width_top = cv2.getTrackbarPos("Width Top","Trackbars")
    height_top = cv2.getTrackbarPos("Height Top","Trackbars")
    width_bottom = cv2.getTrackbarPos("Width Bottom","Trackbars")
    height_bottom = cv2.getTrackbarPos("Height Bottom","Trackbars")
    points = np.float32([(width_top,height_top),(wt-width_top,height_top),
                         (width_bottom,height_bottom),(wt-width_bottom,height_bottom)])
    return points

def draw_points(img,points):
    for x in range(4):
        cv2.circle(img,(int(points[x][0]),int(points[x][1])), 15, (0,0,255), cv2.FILLED)
    return img

def video_capture(url):
    stream = cv2.VideoCapture(url)

    while True:
        r,f = stream.read()
        print(r,f)
        # cv2.imshow("IP camera",f)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.DestroyAllWindows() 

def get_histogram(img,min_percent=0.1,display = False,region = 1):
    
    if region == 1:
        hist_values = np.sum(img,axis = 0)
    else:
        hist_values = np.sum(img[img.shape[0]//region:,:],axis = 0)
    max_value = np.max(hist_values)
    min_value = min_percent * max_value
    
    
    index_array = np.where(hist_values >= min_value)
    base_point = int(np.average(index_array))
    
    if display:
        image_hist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for x,intensity in enumerate(hist_values):
            cv2.line(image_hist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(255,0,255),1)
            cv2.circle(image_hist,(base_point,img.shape[0]),20,(0,255,255),cv2.FILLED)
        return base_point,image_hist
    return base_point

def stack_image(scale, img_array):
    rows = len(img_array)
    columns = len(img_array[0])
    rows_available = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rows_available:
        for x in range(0,rows):
            for y in range(0,columns):
                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0,0), None, scale,scale)
                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]), None, scale, scale)
                if len(img_array[x][y].shape) == 2:
                    img_array[x][y]= cv2.cvtColor(img_array[x][y]   , cv2.COLOR_GRAY2BGR)
        img_blank = np.zeros((height,width,3),np.uint8)
        hor = [img_blank] * rows
        hor_con = [img_blank] * rows
        for x in range(0,rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0,rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x],(0,0),None,scale,scale)
            else:
                    img_array[x] = cv2.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None,scale, scale)
            if len(img_array[x].shape) == 2:
                img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(img_array)
        ver = hor
    return ver

import cv2
import numpy as np

import utils

curve_list = []
avg_list_value = 10 

def get_lane_curve(img,display = 2):
    img_copy = img.copy()
    img_result = img.copy()
    #Step 1 : thresholding
    img_thres = utils.thresholding(img)
    
    #Step 2 : warping
    h,w,c = img.shape
    points = utils.val_trackbars()
    img_warp = utils.wrap_image(img_thres, points, w, h)
    img_warp_points = utils.draw_points(img_copy, points)   
    
    #Step 3: histogram
    mid_point,img_hist = utils.get_histogram(img_warp,display= True,min_percent=0.5,region=4)
    curve_average_point,img_hist = utils.get_histogram(img_warp,display= True,min_percent=0.9)
    curve_raw = curve_average_point - mid_point
    
    #Step 4: 
    curve_list.append(curve_raw)
    if len(curve_list) > avg_list_value:
        curve_list.pop(0)
    curve = 0
    for curves in curve_list:
        curve += int(curves/len(curve_list))
    
    #Step 5:
    if display != 0:
        img_in_warp = utils.wrap_image(img_warp, points, w, h, inv=True)
        img_in_warp = cv2.cvtColor(img_in_warp,cv2.COLOR_GRAY2BGR)
        img_in_warp[0:h//3,0:w] = 0,0,0
        img_lane_color = np.zeros_like(img)
        img_lane_color[:] = 0,255,0
        img_lane_color = cv2.bitwise_and(img_in_warp,img_lane_color)
        img_result = cv2.addWeighted(img_result,1,img_lane_color, 1,0)
        mid_y = 450
        cv2.putText(img_result,str(curve),(w//2 - 80, 85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),1)
        cv2.line(img_result,(w//2,mid_y),(w//2 + (curve * 3), mid_y), (255,0,255,5))
        cv2.line(img_result,((w//2 + (curve * 3)), mid_y - 25), (w//2 + (curve *3), mid_y), (255,0,255))    
        for x in range(-30,30):
            w2 = w//20
            cv2.line(img_result,(w*x + int(curve//50), mid_y - 10),(w * x + int(curve// 50), mid_y + 10), (0,0,255), 2)
        #fps = cv2.getTickFrequency() /(cv2.getTickCount() - timer)
        # cv2.putText(img_result, "FPS", str(int(fps)), (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0 , 255), 1)
    # if display == 2:
    #     img_stacked = utils.stack_image(0.7,([img,img_warp_points,img_warp],[img_hist, img_lane_color, img_result]))
    #     cv2.imshow("ImageStack",img_stacked)
    # elif display == 1:
    #     cv2.imshow("Result", img_result)
    
    curve = curve/100
    if curve > 1: cruve = 1
    if curve< -1: curve = -1
        
    cv2.imshow('Thresh',img_thres)
    cv2.imshow('Warp',img_warp)
    cv2.imshow('Warp Points',img_warp_points)
    cv2.imshow('Histogram',img_hist)
    return curve

if __name__ == "__main__":
    cap = cv2.VideoCapture('http://192.168.29.216:4747/video')
    # cap = utils.video_capture('http://192.168.43.14:4747/video')
    initial_tracebar_vals = [102,80,20,214]
    utils.initialize_trackbars(initial_tracebar_vals)
    frame_counter = 0
    while True:
        frame_counter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
            cap.get(cv2.CAP_PROP_POS_FRAME,0)
            frame_counter = 0
        
        success,img = cap.read()
        img = cv2.resize(img,(480,240))
        get_lane_curve(img)
        cv2.imshow('Vid',img)
        cv2.waitKey(1)
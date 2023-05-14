from motor_module import Motor
from lane_detection import get_lane_curve
import webcam

motor = Motor(2, 3, 4, 17, 22, 27)

def main():
    img = webcam.get_image()
    curve_val = get_lane_curve(img,1)
    
    sen = 1.3
    max_speed = 0.3
    if curve_val>max_speed:
        curve_val = max_speed
    if curve_val<-max_speed:
        curve_val =-max_speed
    print(curve_val)
    if curve_val>0:
        sen =1.7
        if curve_val<0.05: curve_val=0
    else:
        if curve_val>-0.08: curve_val=0
    motor.move(0.5,curve_val*sen,0.05)
    #cv2.waitKey(1)
    
if __name__ == "__main__":
    while True:
        main()
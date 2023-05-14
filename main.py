from motor_module import Motor
from lane_detection import get_lane_curve
import webcam

motor = Motor(2, 3, 4, 17, 22, 27)

def main():
    img = webcam.get_image()
    curve_val = get_lane_curve(img,1)
    
    sen = 1
    max_speed = 0.3
    if curveVal>maxVAl:
        curveVal = maxVAl
    if curveVal<-maxVAl:
        curveVal =-maxVAl
    print(curveVal)
    if curveVal>0:
        sen =1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    motor.move(0.20,-curveVal*sen,0.05)
    #cv2.waitKey(1)
    
if __name__ == "__main__":
    while True:
        main()
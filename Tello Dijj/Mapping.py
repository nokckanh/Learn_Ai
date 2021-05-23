import KeyPressModul as kp
from djitellopy import tello
import numpy as np
import cv2
from time import sleep
import math

##-------------------Phuong Thuc Di Chuyen Trong Map--------------------------
# Toc do chuyen tiep fspeed (Forward speed)
fSpeed = 117 / 10 # Toc do tinh toan voi toc do thuc te khong giong nhau nen lay 11,7 cm/s (thuc te la 15 cm/s) 
aSpeed = 360 / 10 # Toc do goc ( Độ/s)
intervel = 0.25 # Khoang thoi gian 1s thực tế rất lâu nên lấy 0.25 cho nhanh

dIntervel = fSpeed * intervel # Khoảng cách 
aIntervel = aSpeed * intervel # Khoảng góc
#------------------------------------------------------------------


kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

## -------------------------------------------
x, y = 500, 500
a = 0 # Góc
yaw = 0

points = [(0,0), (0,0)]

def getKeyboardInput():
    lr, fb, ud , yv = 0 ,0 ,0, 0
    global x, y, yaw , a
    speed = 15 # cái này là tốc độ chuyển tiếp foward speed
    aspeed = 50
    d = 0

    if kp.getKey("LEFT") : 
        lr = -speed
        d = dIntervel # Khoang cách
        a = -180      # Đặt góc 180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dIntervel # Khoang cách
        a = 180       # Đặt góc 180

    if kp.getKey("UP") : 
        fb = speed
        d = dIntervel 
        a = 270      
    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dIntervel 
        a = -90    

    if kp.getKey("w") : ud = speed
    elif kp.getKey("s"):ud = -speed

    if kp.getKey("a") : 
        yv = -aspeed
        yaw -= aIntervel
    elif kp.getKey("d"):
        yv = aspeed
        yaw += aIntervel

    if kp.getKey("q") : 
        yv = me.land()
    elif kp.getKey("e") : 
        yv = me.takeoff()
    

    sleep(intervel)
    ## Update 
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

#------ Vẽ 1 điểm nhỏ trên cv
def drawPoint(img , points):
    for point in points:
        cv2.circle(img,point,10,(0,0,255),cv2.FILLED)

    cv2.circle(img,points[-1],12,(0,255,0),cv2.FILLED)

    cv2.putText(img, f'({(points[-1][0]- 500)/ 100},{(points[-1][1] - 500) /100})',(points[-1][0] + 10, points[-1][1] + 30),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),1)




while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0] , vals[1], vals[2], vals[3])

    img = np.zeros((1000,1000,3), np.uint8)
    ## Kiểm tra Điểm dừng có = 0 0 
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5])) 
    drawPoint(img, points)
    cv2.imshow("OutPut",img)
    cv2.waitKey(1)
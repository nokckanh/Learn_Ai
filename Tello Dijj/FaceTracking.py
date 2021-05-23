import cv2
import numpy as np
from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 15 , 0)
time.sleep(2.2)

w, h = 450 , 350
fbRange = [6200,6800] ## Phạm vi tiến lùi
pid = [0.4, 0,4, 0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceList = []    
    myFaceListArea = []

    for (x, y, w ,h) in faces :
        cv2.rectangle(img,(x,y),(x + w, y + h),(0,0,255), 2)
        ## Tìm điểm trung tâm
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img,(cx,cy),5,(0,255,0),cv2.FILLED)
        myFaceList.append([cx,cy])
        myFaceListArea.append(area)
    
    if len(myFaceListArea) != 0 :
        i = myFaceList.index(max(myFaceList)) 
        return img , [myFaceList[i], myFaceListArea[i]]
    else:
        return img, [[0 , 0], 0 ]

def trackFace(img, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w/2
    speed = pid[0] * error + pid[1] * (error-pError)
    speed = int(np.clip(speed, -100, 100))


   
    if area > fbRange[0] and  area < fbRange[1] :
        fb = 0
    elif area > fbRange[1] :
        fb = -50
    elif area < fbRange[0] and area != 0:
        fb = 50

    
    if x == 0:
        speed = 0
        error = 0

    me.send_rc_control(0, fb, 0 , speed)
    return error

#cap = cv2.VideoCapture(0)


while True:
   # ret, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img,(w,h))
    img, info = findFace(img)
    pError = trackFace(me , info , w , pid , pError)
    cv2.imshow('Frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
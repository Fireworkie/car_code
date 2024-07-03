import cv2
import numpy as np
import os

# 生成LBPH人脸识别器
recognizer = cv2.face.LBPHFaceRecognizer_create()
# 加载识别器模型
recognizer.read('trainer/trainer.yml')
face_detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')  

# 开启摄像头
cap = cv2.VideoCapture(0) 
cap.set(3, 640)
cap.set(4, 480)

while cap.isOpened():                            
    # 获取一帧图像
    ret, img = cap.read()                                     
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
    faces = face_detector.detectMultiScale(gray, 1.05, minNeighbors=5) 
    for (x, y, w, h) in faces:
         # 用蓝色框标记人脸
         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) 
         # 调整图片大小为112*92
         roi = cv2.resize(gray[y:y+h, x:x+w], (92, 112)) 
         # 人脸预测，返回的id和confidence分别是标签和置信度
         id, confidence = recognizer.predict(roi)
         confidence1 =confidence
         # 置信度评分用来衡量所识别人脸与原模型的差距，0表示完全匹配
         confidence = "{0}%".format(round(100 - confidence))
         cv2.putText(img, "person: " + str(id), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
         cv2.putText(img, "Confidence: " + str(confidence), (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
    cv2.imshow('Recognizing face', img)
    
    # 按ESC键退出
    if cv2.waitKey(10) & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()

import cv2

cap = cv2.VideoCapture(0)  #从摄像头获取图像
cap.set(3, 640) 
cap.set(4, 480) 
face_detector = cv2.CascadeClassifier('cascades\\haarcascade_frontalface_default.xml')
face_id = input('输入人脸样本采集对象的序号： ')
print("请对准摄像头，采集过程中可以改变脸部角度和表情")
#人脸样本数
count = 0   

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.05, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255), 2)
        count += 1
        roi=cv2.resize(gray[y:y+h,x:x+w],(92,112)) #调整到112×92  
#检测到的人脸区域存储对应文件夹
        cv2.imwrite('./dataset/' + str(face_id)  + str(count) + ".jpg", roi)
        cv2.imshow('image', frame)
    k = cv2.waitKey(100) & 0xff  
    if k == 27:  #按'ESC'键退出
        break
    elif count >= 30: #采集30张人脸图像(存在错误的检测)后退出,从中挑选出15张
        break
cap.release()
cv2.destroyAllWindows() 

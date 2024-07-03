import cv2

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# 初始化摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # 获取一帧图像
    ret, frame = cap.read()

    # 使用INTER_AREA插值法将图像的宽与高缩小为原来的一半
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(gray, 1.1, minNeighbors=1)

    for (x, y, w, h) in face_rects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        faceX = x + w // 2
        faceY = y + h // 2
        print("Face detected at ({}, {})\n".format(faceX, faceY))

    cv2.imshow('Face Detector', frame)

    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
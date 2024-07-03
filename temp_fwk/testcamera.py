import cv2

# 打开摄像头
cap = cv2.VideoCapture(0)

# 创建窗口
cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)

while True:
    # 读取摄像头帧
    ret, frame = cap.read()

    # 在窗口中显示帧
    cv2.imshow('Camera', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
import onnxruntime

# 加载模型
ort_session = onnxruntime.InferenceSession('cascades/version-slim-320.onnx')
input_name = ort_session.get_inputs()[0].name
output_name = ort_session.get_outputs()[0].name

# 视频捕获，可以替换为具体的视频文件路径以处理视频文件
cap = cv2.VideoCapture(0)  # 使用0表示默认摄像头

while True:
    # 读取视频帧
    ret, frame = cap.read()
    if not ret:
        break  # 如果无法读取帧则退出循环

    # 预处理
    img_resized = cv2.resize(frame, (320, 240))
    img_data = img_resized.astype(np.float32) / 255.0
    img_data = np.expand_dims(img_data, axis=0)
    img_data = np.squeeze(img_data, axis=0)  # 移除第0维度，现在形状变为 (height, width, channels)
    # 然后转置维度，以得到 (channels, height, width)
    img_data = img_data.transpose((2, 0, 1))
    img_data = np.expand_dims(img_data, axis=0)

    # 执行推理
    ort_inputs = {input_name: img_data}
    outputs = ort_session.run([output_name], ort_inputs)

    # 解析输出并绘制人脸框
    detections = outputs[0]
    for detection in detections:
        bbox = detection[:4]  # 假设detection是一个包含多个值的数组，前四个值对应一个边界框  # 确保bbox是长度为4的数组
        xmin, ymin, xmax, ymax = bbox.astype(int)  # 直接转换整个边界框数组为整数
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # 显示结果
    cv2.imshow('Real-time Face Detection', frame)

    # 按'q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
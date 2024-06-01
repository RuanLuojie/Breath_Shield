from flask import Flask, jsonify, request
import cv2
import numpy as np
import torch
import os

app = Flask(__name__)

# 確保這裡的路徑是你模型文件的絕對路徑
model_path = r'best.pt'

# 檢查模型文件是否存在
if not os.path.exists(model_path):
    raise Exception(f"Model file not found at {model_path}")

# 加載YOLOv5模型並強制重新加載
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

# 初始化攝像頭變量
camera_ip = None
camera = None

def initialize_camera(ip):
    global camera
    if camera:
        camera.release()
    camera = cv2.VideoCapture(f'http://{ip}:5000/video_feed')
    if not camera.isOpened():
        camera = None
        return False
    return True

def get_prediction():
    global camera
    if camera is None:
        return None

    try:
        # 從攝像頭抓取影像
        ret, image = camera.read()
        if not ret:
            return None

        # YOLOv5 推理
        results = model(image)

        # 解析結果
        detected_classes = results.pandas().xyxy[0]['name'].values
        detected_confidences = results.pandas().xyxy[0]['confidence'].values

        if len(detected_classes) > 0:
            class_name = detected_classes[0]
            confidence_score = detected_confidences[0]
        else:
            class_name = "No object detected"
            confidence_score = 0.0

        return {
            "class_name": class_name,
            "confidence_score": f"{np.round(confidence_score * 100, 2)}%"
        }
    except Exception as e:
        # 捕獲任何異常並忽略
        print(f"Error during prediction: {e}")
        return None

@app.route('/set_camera_ip', methods=['POST'])
def set_camera_ip():
    global camera_ip
    try:
        data = request.json
        camera_ip = data.get('camera_ip')
        if camera_ip and initialize_camera(camera_ip):
            return jsonify({"status": "success", "camera_ip": camera_ip})
        else:
            raise Exception("No IP address provided or could not initialize camera")
    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)}), 500

@app.route('/predict', methods=['GET'])
def predict():
    try:
        if camera is None:
            raise Exception("Camera not initialized")

        result = get_prediction()
        if result:
            return jsonify(result)
        else:
            raise Exception("Could not read from camera")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8080, host='0.0.0.0')

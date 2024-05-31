from flask import Flask, jsonify, request
import cv2
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# 禁用科学计数法
np.set_printoptions(suppress=True)

# 加载模型和标签
model = load_model("keras_Model.h5", compile=False)
class_names = [name.strip() for name in open("labels.txt", "r").readlines()]

# 初始化摄像头变量
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

    # 从摄像头抓取影像
    ret, image = camera.read()
    if not ret:
        return None

    # 调整影像大小
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # 将影像转为numpy数组并调整为模型输入的形状
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # 标准化影像数组
    image = (image / 127.5) - 1

    # 预测模型
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return {
        "class_name": class_name.strip(),
        "confidence_score": f"{np.round(confidence_score * 100, 2)}%"
    }

@app.route('/set_camera_ip', methods=['POST'])
def set_camera_ip():
    global camera_ip
    data = request.json
    camera_ip = data.get('camera_ip')
    if camera_ip and initialize_camera(camera_ip):
        return jsonify({"status": "success", "camera_ip": camera_ip})
    else:
        return jsonify({"status": "failure", "message": "No IP address provided or could not initialize camera"}), 400

@app.route('/predict', methods=['GET'])
def predict():
    if camera is None:
        return jsonify({"error": "Camera not initialized"}), 400
    
    result = get_prediction()
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Could not read from camera"}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8080, host='0.0.0.0')

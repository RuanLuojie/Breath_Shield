from flask import Flask, Response, jsonify
import cv2
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model and labels
model = load_model(r"keras_model.h5", compile=False)
class_names = [name.strip() for name in open(r"labels.txt", "r").readlines()]

# Initialize the video camera
camera = cv2.VideoCapture(0)

def get_prediction(frame):
    # Process and predict
    processed_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    processed_frame = np.asarray(processed_frame, dtype=np.float32).reshape(1, 224, 224, 3)
    processed_frame = (processed_frame / 127.5) - 1
    prediction = model.predict(processed_frame)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = np.round(prediction[0][index] * 100, 2)

    return {
        "class_name": class_name,
        "confidence_score": f"{confidence_score}%"
    }

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        # Get predictions for the current frame
        prediction = get_prediction(frame)
        # You can modify how you use the prediction here, e.g., display it on the frame
        cv2.putText(frame, f"{prediction['class_name']}: {prediction['confidence_score']}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/predict')
def predict():
    # This endpoint might be redundant now, as predictions are made in real-time and displayed on the video
    frame = camera.read()[1]
    result = get_prediction(frame)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8080, host='0.0.0.0')

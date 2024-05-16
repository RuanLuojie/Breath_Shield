
import numpy as np
import cv2
import tflite_runtime.interpreter as tflite

class TFLiteModel:
    def __init__(self, model_path, labels_path):
        # Load TFLite model and allocate tensors
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        # Load labels
        self.class_names = self.load_labels(labels_path)

    def load_labels(self, path):
        with open(path, "r") as f:
            return [line.strip() for line in f.readlines()]

    def predict(self, image):
        # Preprocess the image for the model
        input_shape = self.input_details[0]['shape']
        image_resized = cv2.resize(image, (input_shape[1], input_shape[2]), interpolation=cv2.INTER_AREA)
        input_data = np.expand_dims(image_resized, axis=0).astype(np.float32)
        input_data = (input_data / 127.5) - 1

        # Perform prediction
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

        # Interpret the results
        index = np.argmax(output_data)
        return self.class_names[index], output_data[0][index]

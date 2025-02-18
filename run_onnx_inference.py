#!/usr/bin/env python
"""Script to run inference using the YOLO ONNX model via onnxruntime.
Usage:
    python run_onnx_inference.py

Ensure that 'yolov8s.onnx' is in the current directory. If not, please run 'download_yolo_models_onnx.py' first to generate the ONNX model.
"""

import os
import cv2
import numpy as np
import onnxruntime as ort


def preprocess_image(image_path, input_shape=(640, 640)):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image {image_path}")
    # Convert from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Resize image
    img = cv2.resize(img, input_shape)
    # Normalize image to [0,1]
    img = img.astype(np.float32) / 255.0
    # Transpose to CHW
    img = np.transpose(img, (2, 0, 1))
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    return img


def main():
    model_file = "yolov8s.onnx"
    if not os.path.exists(model_file):
        print(f"ONNX model file '{model_file}' not found. Please run 'download_yolo_models_onnx.py' first to generate it.")
        return

    # Create an ONNX runtime session
    sess = ort.InferenceSession(model_file)
    input_name = sess.get_inputs()[0].name
    print(f"Model input name: {input_name}")

    # Use a sample image from the 'samples' folder
    image_file = os.path.join("samples", "bus.jpg")
    if not os.path.exists(image_file):
        print(f"Sample image '{image_file}' not found. Please ensure the image exists.")
        return

    # Preprocess the image
    input_tensor = preprocess_image(image_file)
    print(f"Input tensor shape: {input_tensor.shape}")

    # Run inference using the ONNX runtime
    outputs = sess.run(None, {input_name: input_tensor})
    print("Inference outputs:")
    for idx, output in enumerate(outputs):
        print(f"Output {idx}: shape {output.shape}")


if __name__ == "__main__":
    main() 
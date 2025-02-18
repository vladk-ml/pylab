#!/usr/bin/env python
"""GUI App for ONNX-Based YOLO Inference

Usage:
    python gui_onnx_inference_app.py

Ensure that 'yolov8s.onnx' is in the current directory (export it first if needed).
"""

import os
import cv2
import numpy as np
import onnxruntime as ort
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# Preprocess the image: load, resize, normalize, and format as CHW

def preprocess_image(image_path, input_shape=(640, 640)):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image {image_path}")
    # Convert from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Resize image
    img = cv2.resize(img, input_shape)
    # Normalize to [0,1]
    img = img.astype(np.float32) / 255.0
    # Transpose to CHW and add batch dimension
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img


# Function to perform inference using onnxruntime

def run_inference(model_file, image_path):
    sess = ort.InferenceSession(model_file)
    input_name = sess.get_inputs()[0].name
    input_tensor = preprocess_image(image_path)
    outputs = sess.run(None, {input_name: input_tensor})
    return outputs


class ONNXInferenceApp:
    def __init__(self, master):
        self.master = master
        master.title("ONNX Inference App")

        self.image_path = None
        self.model_file = "yolov8s.onnx"

        # Check for ONNX model
        if not os.path.exists(self.model_file):
            messagebox.showerror("Error", f"Model file '{self.model_file}' not found. Please export the model first.")

        # UI Elements
        self.img_label = tk.Label(master, text="No image loaded")
        self.img_label.pack(pady=10)

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5)

        self.infer_button = tk.Button(master, text="Run Inference", command=self.run_inference_ui)
        self.infer_button.pack(pady=5)

        self.results_label = tk.Label(master, text="Inference results will appear here")
        self.results_label.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(initialdir="samples", title="Select Image",
                                               filetypes=( ("Image Files", "*.jpg;*.png;*.jpeg"), ("All Files", "*.*") ))
        if file_path:
            self.image_path = file_path
            try:
                img = Image.open(file_path)
                img = img.resize((400, 300))  # Resize for display
                self.photo = ImageTk.PhotoImage(img)
                self.img_label.configure(image=self.photo, text="")
                self.img_label.image = self.photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def run_inference_ui(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please load an image first.")
            return
        try:
            outputs = run_inference(self.model_file, self.image_path)
            result_text = "Inference outputs:\n"
            for idx, output in enumerate(outputs):
                result_text += f"Output {idx}: shape {output.shape}\n"
            self.results_label.config(text=result_text)
        except Exception as e:
            messagebox.showerror("Inference Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ONNXInferenceApp(root)
    root.mainloop() 
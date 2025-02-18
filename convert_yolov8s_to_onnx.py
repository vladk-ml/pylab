#!/usr/bin/env python
"""Script to convert YOLOv8 small model from PyTorch (.pt) to ONNX format.
Usage:
    python convert_yolov8s_to_onnx.py

Ensure that you have the 'ultralytics' package installed and that 'yolov8s.pt' 
is accessible (in the current directory or update the path accordingly).
"""

try:
    from ultralytics import YOLO
except ImportError:
    raise ImportError("The ultralytics package is required. Please install it via 'pip install ultralytics'.")


def main():
    pt_model_file = "yolov8s.pt"
    onnx_model_file = "yolov8s.onnx"

    print(f"Loading YOLOv8 small model from {pt_model_file}...")
    model = YOLO(pt_model_file)

    print("Exporting model to ONNX format...")
    # This will export the model as 'yolov8s.onnx' to the current directory
    model.export(format="onnx", simplify=True, project=".", name="yolov8s")

    print(f"Export complete. The ONNX model should be available as {onnx_model_file}.")


if __name__ == "__main__":
    main() 
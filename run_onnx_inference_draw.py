#!/usr/bin/env python
"""Script to run inference using the YOLO ONNX model, post-process detections, and draw output bounding boxes.

Usage:
    python run_onnx_inference_draw.py

Ensure that 'yolov8s.onnx' is in the current directory and that a sample image (e.g., samples/bus.jpg) exists.
"""

import os
import cv2
import numpy as np
import onnxruntime as ort

# Parameters
INPUT_SIZE = (640, 640)
CONF_THRESHOLD = 0.25
IOU_THRESHOLD = 0.45


def preprocess_image_cv(image, input_shape=INPUT_SIZE):
    """Resize and normalize the image for model input."""
    # Resize image
    resized = cv2.resize(image, input_shape)
    # Convert BGR to RGB
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    # Normalize to [0,1]
    img = rgb.astype(np.float32) / 255.0
    # Convert HWC to CHW
    img = np.transpose(img, (2, 0, 1))
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    return img


def xywh_to_xyxy(box):
    """Convert [center_x, center_y, w, h] to [x1, y1, x2, y2]."""
    cx, cy, w, h = box
    x1 = cx - w / 2
    y1 = cy - h / 2
    x2 = cx + w / 2
    y2 = cy + h / 2
    return [x1, y1, x2, y2]


def compute_iou(box1, box2):
    """Compute Intersection over Union for two boxes in [x1, y1, x2, y2] format."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = max(0, box1[2] - box1[0]) * max(0, box1[3] - box1[1])
    area2 = max(0, box2[2] - box2[0]) * max(0, box2[3] - box2[1])
    union = area1 + area2 - inter_area
    if union == 0:
        return 0
    return inter_area / union


def non_max_suppression(boxes, scores, iou_threshold=IOU_THRESHOLD):
    """Simple non-max suppression implementation."""
    indices = sorted(range(len(boxes)), key=lambda i: scores[i], reverse=True)
    keep = []
    while indices:
        current = indices.pop(0)
        keep.append(current)
        indices = [i for i in indices if compute_iou(boxes[current], boxes[i]) < iou_threshold]
    return keep


def postprocess(outputs, conf_threshold=CONF_THRESHOLD):
    """Post-process raw model outputs to extract detections and apply NMS.

    Assumes outputs is a list with at least one element. The first element should have shape (1, 84, 8400),
    where 84 = 4 (box) + 1 (objectness) + 79 (class scores).
    """
    raw = outputs[0]  # shape: (1, 84, 8400)
    # Remove batch dimension and transpose to (8400, 84)
    preds = np.squeeze(raw, axis=0).transpose(1, 0)  # shape: (8400, 84)

    boxes = []
    scores = []
    class_ids = []

    for pred in preds:
        # The first 4 are bbox (assumed to be in xywh format), next is objectness, rest are class scores
        box = pred[0:4]
        obj_conf = pred[4]
        class_scores = pred[5:]
        cls_id = np.argmax(class_scores)
        cls_conf = class_scores[cls_id]
        score = obj_conf * cls_conf
        if score >= conf_threshold:
            # Convert box from xywh to xyxy
            box_xyxy = xywh_to_xyxy(box)
            boxes.append(box_xyxy)
            scores.append(score)
            class_ids.append(cls_id)

    if len(boxes) == 0:
        return [], [], []

    boxes = np.array(boxes)
    scores = np.array(scores)
    class_ids = np.array(class_ids)

    # Apply non-max suppression
    keep_indices = non_max_suppression(boxes, scores, iou_threshold=IOU_THRESHOLD)

    return boxes[keep_indices], scores[keep_indices], class_ids[keep_indices]


def draw_detections(image, boxes, scores, class_ids):
    """Draw bounding boxes and scores on the image."""
    for box, score, cls in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f'{score:.2f}'  # You can also add class label if desired
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    return image


def main():
    model_file = "yolov8s.onnx"
    sample_image_path = os.path.join("samples", "bus.jpg")

    if not os.path.exists(model_file):
        print(f"ONNX model file '{model_file}' not found. Please export the model first.")
        return

    if not os.path.exists(sample_image_path):
        print(f"Sample image '{sample_image_path}' not found.")
        return

    # Load the model
    sess = ort.InferenceSession(model_file)
    input_name = sess.get_inputs()[0].name

    # Read and preprocess image
    orig_image = cv2.imread(sample_image_path)
    if orig_image is None:
        print(f"Failed to load image {sample_image_path}")
        return
    # For inference, resize and preprocess the image
    input_tensor = preprocess_image_cv(orig_image, INPUT_SIZE)

    # Run inference
    outputs = sess.run(None, {input_name: input_tensor})

    # Post-process detections
    boxes, scores, class_ids = postprocess(outputs, CONF_THRESHOLD)

    # For drawing, use the resized image (for consistency with inference)
    drawn_image = cv2.resize(orig_image, INPUT_SIZE)
    drawn_image = draw_detections(drawn_image, boxes, scores, class_ids)

    # Display the image
    cv2.imshow('Detections', drawn_image)
    print("Press any key in the image window to exit...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main() 
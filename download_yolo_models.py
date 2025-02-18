#!/usr/bin/env python
"""Script to download YOLO models (nano and small) and sample demo images.
Usage:
    pyinstaller --onefile download_yolo_models.py
"""

import os
import urllib.request
try:
    from ultralytics import YOLO
except ImportError:
    raise ImportError("The ultralytics package is required. Please install it.")


def download_image(image_url, dest_path):
    if not os.path.exists(dest_path):
        print(f"Downloading image from {image_url} to {dest_path}")
        urllib.request.urlretrieve(image_url, dest_path)
    else:
        print(f"Image {dest_path} already exists.")


def main():
    # Load and thereby download YOLO nano and small models
    print("Loading YOLO nano model...")
    model_nano = YOLO("yolov8n.pt")
    print("Loading YOLO small model...")
    model_small = YOLO("yolov8s.pt")

    # Create a directory for sample images
    os.makedirs("samples", exist_ok=True)

    # Define sample image URLs
    bus_url = "https://ultralytics.com/images/bus.jpg"
    zidane_url = "https://ultralytics.com/images/zidane.jpg"
    sportscast_url = "https://ultralytics.com/images/sportscast.jpg"

    # Download sample images
    download_image(bus_url, os.path.join("samples", "bus.jpg"))
    download_image(zidane_url, os.path.join("samples", "zidane.jpg"))
    try:
        download_image(sportscast_url, os.path.join("samples", "sportscast.jpg"))
    except Exception as e:
        print(f"Failed to download sportscast.jpg: {e}")


if __name__ == "__main__":
    main() 
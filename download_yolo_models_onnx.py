import os
import urllib.request

try:
    from ultralytics import YOLO
except ImportError:
    raise ImportError("The ultralytics package is required. Please install it.")

try:
    import onnxruntime as ort
except ImportError:
    raise ImportError("The onnxruntime package is required. Please install it.")


def download_image(image_url, dest_path):
    if not os.path.exists(dest_path):
        print(f"Downloading image from {image_url} to {dest_path}")
        urllib.request.urlretrieve(image_url, dest_path)
    else:
        print(f"Image {dest_path} already exists.")


def main():
    onnx_model_file = "yolov8s.onnx"
    # Check if the ONNX model exists; if not, export it from the PyTorch model
    if not os.path.exists(onnx_model_file):
        print("ONNX model not found, exporting from the PyTorch model...")
        model = YOLO("yolov8s.pt")
        # Export to ONNX format; this should create an ONNX file in the current directory
        model.export(format="onnx", simplify=True)
        
        # Confirm the file exists, or attempt to rename an exported ONNX file
        if not os.path.exists(onnx_model_file):
            for file in os.listdir('.'):
                if file.endswith('.onnx'):
                    os.rename(file, onnx_model_file)
                    print(f"Renamed {file} to {onnx_model_file}")
                    break
    else:
        print("ONNX model already exists.")
    
    # Load the ONNX model using onnxruntime
    try:
        sess = ort.InferenceSession(onnx_model_file)
        print("Successfully loaded the ONNX model with onnxruntime.")
    except Exception as e:
        print(f"Failed to load the ONNX model: {e}")

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
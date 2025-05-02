import torch
import cv2
import os

# Load YOLOv5 model (from PyTorch Hub)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Set model to evaluation mode
model.eval()

def detect_and_annotate(image_path, output_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image.")
        return

    # Convert image from BGR (OpenCV format) to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform detection
    results = model(img_rgb)

    # Parse results
    detections = results.xyxy[0]  # [x1, y1, x2, y2, confidence, class]

    if len(detections) == 0:
        print("No objects detected in the image.")
        return

   
        # Get class names
    class_names = results.names

    # Print the number of detections
    print(f"Number of objects detected: {len(detections)}")

    # Draw bounding boxes
    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        class_id = int(cls)
        label = f"{class_names[class_id]} {conf:.2f}"

        # Draw rectangle and put label
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the output image
    cv2.imwrite(output_path, img)
    print(f"Annotated image saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    input_image = "input.jpg"         # Replace with your image path
    output_image = "output_annotated.jpg"
    detect_and_annotate(input_image, output_image)

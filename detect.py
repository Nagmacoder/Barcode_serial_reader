import cv2
from ultralytics import YOLO
import easyocr
import os
import csv
from utils import correct_serial

# Setup folders
os.makedirs('output/cropped', exist_ok=True)

# Load AI models
barcode_model = YOLO('barcode_model/yolov8n.pt')
ocr_reader = easyocr.Reader(['en'])

# Process images
with open('output/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Image', 'Serial Number'])
    
    for img_name in os.listdir('input_images'):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = cv2.imread(f'input_images/{img_name}')
            results = barcode_model(img)
            
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cropped = img[y1:y2+50, x1:x2]  # Crop barcode + area below
                cv2.imwrite(f'output/cropped/{img_name}_crop.jpg', cropped)
                
                # Read text
                text_results = ocr_reader.readtext(cropped)
                serial = " ".join([res[1] for res in text_results if res[2] > 0.4])
                serial = correct_serial(serial)  # Apply corrections
                
                writer.writerow([img_name, serial])
                print(f"Found in {img_name}: {serial}")
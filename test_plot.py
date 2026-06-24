import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("yolov8n.pt") # use standard model for testing if PCB model requires image to have pcbs

img = np.zeros((640, 640, 3), dtype=np.uint8)
cv2.rectangle(img, (100, 100), (200, 200), (255, 255, 255), -1)

results = model(img)
if len(results[0].boxes) > 0:
    data = results[0].boxes.data
    w_half = (data[:, 2] - data[:, 0]) / 2.0
    h_half = (data[:, 3] - data[:, 1]) / 2.0
    
    data[:, 0] += w_half
    data[:, 2] += w_half
    data[:, 1] += h_half
    data[:, 3] += h_half

try:
    plotted = results[0].plot()
    print("Success!")
except Exception as e:
    print("Plot failed:", e)

import numpy as np
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
img = np.zeros((640, 640, 3), dtype=np.uint8)
img[100:200, 100:200] = 255  # draw a block to trigger detection

results = model(img)
if len(results[0].boxes) > 0:
    data = results[0].boxes.data.clone()
    w_half = (data[:, 2] - data[:, 0]) / 2.0
    h_half = (data[:, 3] - data[:, 1]) / 2.0
    data[:, 0] += w_half
    data[:, 2] += w_half
    data[:, 1] += h_half
    data[:, 3] += h_half
    
    results[0].update(boxes=data)

plotted = results[0].plot()
print("Success!")

from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data="C:/Projects/PCB/datasets/data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        device=0
    )

if __name__ == "__main__":
    main()
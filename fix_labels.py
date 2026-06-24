import os
import cv2

base_path = r"C:\Projects\PCB\datasets"

splits = ["train", "valid", "test"]

for split in splits:
    label_dir = os.path.join(base_path, split, "labels")
    image_dir = os.path.join(base_path, split, "images")

    print(f"Processing {split}...")

    for file in os.listdir(label_dir):
        if file.endswith(".txt"):
            label_path = os.path.join(label_dir, file)
            image_path = os.path.join(image_dir, file.replace(".txt", ".jpg"))

            # read image
            img = cv2.imread(image_path)
            if img is None:
                continue

            h, w, _ = img.shape

            with open(label_path, "r") as f:
                lines = f.readlines()

            new_lines = []

            for line in lines:
                parts = line.strip().split()

                if len(parts) == 5:
                    x1, y1, x2, y2, cls = map(int, parts)

                    # convert class (1–6 → 0–5)
                    cls = cls - 1

                    # convert bbox
                    x_center = ((x1 + x2) / 2) / w
                    y_center = ((y1 + y2) / 2) / h
                    bw = (x2 - x1) / w
                    bh = (y2 - y1) / h

                    new_lines.append(f"{cls} {x_center} {y_center} {bw} {bh}")

            with open(label_path, "w") as f:
                f.write("\n".join(new_lines))

print("DONE ✅")
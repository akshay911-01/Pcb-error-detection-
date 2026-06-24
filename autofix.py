import os
import cv2

print("🔥 Autofix started...")

DATASET_PATH = r"C:\Projects\PCB\datasets"
splits = ["train", "valid", "test"]

total_fixed = 0
total_skipped = 0

for split in splits:
    img_dir = os.path.join(DATASET_PATH, split, "images")
    lbl_dir = os.path.join(DATASET_PATH, split, "labels")

    print(f"\n📂 Checking {split}...")

    for file in os.listdir(lbl_dir):
        if not file.endswith(".txt"):
            continue

        label_path = os.path.join(lbl_dir, file)
        image_path = os.path.join(img_dir, file.replace(".txt", ".jpg"))

        if not os.path.exists(image_path):
            image_path = image_path.replace(".jpg", ".png")

        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Image missing: {file}")
            continue

        h, w, _ = img.shape

        new_lines = []
        changed = False

        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            cls, x, y, bw, bh = map(float, parts)

            # 🧠 CHECK if already normalized
            if all(0 <= v <= 1 for v in [x, y, bw, bh]):
                new_lines.append(line)
                total_skipped += 1
                continue

            # 🔧 Convert pixel → normalized
            x /= w
            y /= h
            bw /= w
            bh /= h

            # Clamp safety
            x = min(max(x, 0), 1)
            y = min(max(y, 0), 1)
            bw = min(max(bw, 0), 1)
            bh = min(max(bh, 0), 1)

            new_lines.append(f"{int(cls)} {x} {y} {bw} {bh}\n")
            changed = True

        if changed:
            print(f"🔧 Fixed: {file}")
            total_fixed += 1

            with open(label_path, "w") as f:
                f.writelines(new_lines)

print("\n📊 SUMMARY")
print(f"✅ Fixed files: {total_fixed}")
print(f"⏭️ Skipped (already correct): {total_skipped}")
print("🚀 Autofix completed!")
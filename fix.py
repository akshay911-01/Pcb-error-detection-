import os
import cv2

DATASET_PATH = r"C:\Projects\PCB\datasets"

splits = ["train", "val", "test"]

total_images = 0
total_labels = 0
missing_labels = 0
invalid_labels = 0
corrupt_images = 0

print("\n🔍 Checking dataset...\n")

for split in splits:
    img_dir = os.path.join(DATASET_PATH, split, "images")
    lbl_dir = os.path.join(DATASET_PATH, split, "labels")

    print(f"\n📂 Checking {split}...")

    images = os.listdir(img_dir)

    for img_file in images:
        if not img_file.endswith((".jpg", ".png", ".jpeg")):
            continue

        total_images += 1

        img_path = os.path.join(img_dir, img_file)
        label_file = img_file.rsplit(".", 1)[0] + ".txt"
        label_path = os.path.join(lbl_dir, label_file)

        # 🧠 Check image validity
        img = cv2.imread(img_path)
        if img is None:
            print(f"❌ Corrupt image: {img_file}")
            corrupt_images += 1

        # 🧠 Check label existence
        if not os.path.exists(label_path):
            print(f"⚠️ Missing label: {img_file}")
            missing_labels += 1
            continue

        total_labels += 1

        # 🧠 Check label format
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()

            if len(parts) != 5:
                print(f"❌ Invalid label format in {label_file}")
                invalid_labels += 1
                continue

            try:
                cls, x, y, w, h = map(float, parts)

                # Check bounds
                if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                    print(f"❌ Out of bounds values in {label_file}")
                    invalid_labels += 1

                if cls < 0:
                    print(f"❌ Invalid class id in {label_file}")
                    invalid_labels += 1

            except:
                print(f"❌ Non-numeric label in {label_file}")
                invalid_labels += 1


# 🧾 FINAL REPORT
print("\n📊 DATASET REPORT")
print(f"Total Images: {total_images}")
print(f"Total Labels: {total_labels}")
print(f"Missing Labels: {missing_labels}")
print(f"Invalid Labels: {invalid_labels}")
print(f"Corrupt Images: {corrupt_images}")

if missing_labels == 0 and invalid_labels == 0 and corrupt_images == 0:
    print("\n✅ DATASET IS CLEAN — READY FOR TRAINING 🚀")
else:
    print("\n⚠️ FIX ISSUES BEFORE TRAINING (or YOLO will cry 💀)")
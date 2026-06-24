import os

label_path = r"C:\Projects\PCB\datasets\train\labels"

for file in os.listdir(label_path):
    if file.endswith(".txt"):
        path = os.path.join(label_path, file)
        
        with open(path, "r") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0:
                cls = int(parts[0]) % 6  # force into 0–5
                parts[0] = str(cls)
                new_lines.append(" ".join(parts))
        
        with open(path, "w") as f:
            f.write("\n".join(new_lines))
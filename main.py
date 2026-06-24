from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from fastapi.responses import FileResponse
import numpy as np
import cv2
from PIL import Image
import io
import base64
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

app = FastAPI()

# ✅ CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = YOLO("runs/detect/train12/weights/best.pt")

last_counts = {}
last_detections = []

# 🧠 DEFECT DESCRIPTIONS
defect_info = {
    "open_circuit": "A break in the conductive path that prevents current flow.",
    "short": "Unintended connection between two conductive paths.",
    "missing_hole": "Absence of a required drill hole affecting connectivity.",
    "spur": "Unwanted small copper projection causing interference.",
    "spurious_copper": "Extra copper leading to incorrect circuit behavior.",
    "mouse_bite": "Irregular edges causing weak connections."
}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global last_counts

    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = model(img, conf=0.6)

        # Reverting shift mathematics
        plotted = results[0].plot()

        # Save output image for the report
        cv2.imwrite("output.jpg", plotted)

        _, buffer = cv2.imencode(".jpg", plotted)
        img_base64 = base64.b64encode(buffer).decode()

        labels = results[0].boxes.cls.cpu().numpy()
        confs = results[0].boxes.conf.cpu().numpy()
        boxes = results[0].boxes.xywh.cpu().numpy()
        names = model.names

        global last_detections
        last_detections = []
        for i in range(len(labels)):
            last_detections.append({
                "class": str(names[int(labels[i])]),
                "conf": float(confs[i]),
                "x": int(boxes[i][0]),
                "y": int(boxes[i][1]),
                "w": int(boxes[i][2]),
                "h": int(boxes[i][3])
            })

        from collections import Counter
        counts = Counter([d["class"] for d in last_detections])
        last_counts = counts

        return {
            "image": img_base64,
            "detections": [{"class": k, "count": v} for k, v in counts.items()]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "image": "", 
            "detections": [{"class": f"ERROR: {str(e)}", "count": 1}]
        }

@app.get("/report")
def report():
    doc = SimpleDocTemplate("report.pdf", pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    content = []

    # Format header
    content.append(Paragraph("PCB Defect Detection Report", styles["Title"]))
    content.append(Paragraph(f"<font color=\"#6b7280\">Generated: {datetime.datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}</font>", styles["Normal"]))
    content.append(Spacer(1, 20))

    if not last_detections:
        content.append(Paragraph("No defects detected. The PCB appears healthy.", styles['Heading3']))
        doc.build(content)
        return FileResponse("report.pdf", media_type="application/pdf", filename="report.pdf")

    # Summary Stats
    total_defects = len(last_detections)
    defect_classes = len(last_counts)
    avg_conf = sum(d["conf"] for d in last_detections) / total_defects if total_defects > 0 else 0

    metrics_data = [[
        Paragraph(f"<font color=\"#6b7280\">TOTAL DEFECTS</font><br/><font size=\"16\" color=\"#2563eb\"><b>{total_defects}</b></font>", styles["Normal"]),
        Paragraph(f"<font color=\"#6b7280\">DEFECT CLASSES</font><br/><font size=\"16\" color=\"#2563eb\"><b>{defect_classes}</b></font>", styles["Normal"]),
        Paragraph(f"<font color=\"#6b7280\">AVG. CONFIDENCE</font><br/><font size=\"16\" color=\"#2563eb\"><b>{avg_conf * 100:.1f}%</b></font>", styles["Normal"])
    ]]

    metrics_table = Table(metrics_data, colWidths=[180, 180, 180])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f3f4f6")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.white),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    content.append(metrics_table)
    content.append(Spacer(1, 20))

    # Defect Class Distribution
    content.append(Paragraph("<b>Defect Class Distribution</b>", styles['Heading3']))
    content.append(Spacer(1, 10))
    
    dist_data = [["DEFECT CLASS", "COUNT", "PERCENTAGE"]]
    for k, v in defect_info.items():
        count = last_counts.get(k, 0)
        perc = (count / total_defects) * 100 if total_defects > 0 else 0
        dist_data.append([k.replace("_", " ").title(), str(count), f"{perc:.1f}%"])

    dist_table = Table(dist_data, colWidths=[200, 170, 170])
    dist_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f9fafb")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#6b7280")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    content.append(dist_table)
    content.append(Spacer(1, 20))

    # Individual Detections
    content.append(Paragraph("<b>Individual Detections</b>", styles['Heading3']))
    content.append(Spacer(1, 10))

    det_data = [["#", "CLASS", "CONFIDENCE", "LOCATION (X, Y)", "SIZE (W x H)"]]
    for idx, d in enumerate(last_detections, 1):
        det_data.append([
            str(idx),
            d["class"].replace("_", " ").title(),
            f"{d['conf'] * 100:.1f}%",
            f"{d['x']}, {d['y']}",
            f"{d['w']} x {d['h']}"
        ])

    # Allow table to split across pages
    det_table = Table(det_data, colWidths=[40, 150, 110, 120, 120], repeatRows=1)
    det_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f9fafb")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#6b7280")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    content.append(det_table)

    doc.build(content)

    return FileResponse("report.pdf", media_type="application/pdf", filename="report.pdf")
from flask import Flask, render_template, request, send_file
from ultralytics import YOLO
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
model = YOLO("runs/detect/train/weights/best.pt")

UPLOAD_FOLDER = "static/uploads"
REPORT_PATH = "static/report.pdf"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# 🧠 DEFECT DESCRIPTIONS
defect_info = {
    "open_circuit": "A break in the conductive path that prevents current flow.",
    "short": "Unintended connection between two conductive paths.",
    "missing_hole": "Absence of a required drill hole affecting connectivity.",
    "spur": "Unwanted small copper projection causing interference.",
    "spurious_copper": "Extra copper leading to incorrect circuit behavior.",
    "mouse_bite": "Irregular edges causing weak connections."
}


# 🧾 PDF GENERATOR
def generate_pdf(output_image, detected_classes):
    doc = SimpleDocTemplate(REPORT_PATH)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("PCB Defect Detection Report", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Detected Output Image:", styles['Heading2']))
    content.append(Spacer(1, 10))
    content.append(Image(output_image, width=400, height=300))
    content.append(Spacer(1, 20))

    if detected_classes:
        content.append(Paragraph("Detected Defects:", styles['Heading2']))
        content.append(Spacer(1, 10))

        for defect in detected_classes:
            desc = defect_info.get(defect, "No description available.")
            content.append(Paragraph(f"<b>{defect}</b>", styles['Heading3']))
            content.append(Paragraph(desc, styles['BodyText']))
            content.append(Spacer(1, 12))
    else:
        content.append(Paragraph("No defects detected.", styles['BodyText']))

    content.append(Spacer(1, 20))
    content.append(Paragraph("Conclusion:", styles['Heading2']))
    content.append(Paragraph(
        "The PCB has been analyzed using a YOLO-based object detection model. "
        "The system automatically identifies defects and generates this report for inspection purposes.",
        styles['BodyText']
    ))

    doc.build(content)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]

        # Save uploaded file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Run YOLO
        results = model(filepath)

        # Save output image
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "output.jpg")
        results[0].save(output_path)

        # 🧠 Extract detected classes
        classes = results[0].boxes.cls.tolist() if results[0].boxes else []
        names = model.names
        detected_classes = [names[int(c)] for c in classes]

        # Generate PDF
        generate_pdf(output_path, detected_classes)

        return render_template(
            "index.html",
            input=filepath,
            output=output_path,
            report=REPORT_PATH,
            defects=detected_classes
        )

    return render_template("index.html")


# 📥 DOWNLOAD REPORT
@app.route("/download")
def download():
    return send_file(REPORT_PATH, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
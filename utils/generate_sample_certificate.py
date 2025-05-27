from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_sample_certificate(cert_type):
    sample_text = {
        "barangay_clearance": "Barangay Clearance",
        "indigency": "Certificate of Indigency",
        "residency": "Certificate of Residency",
    }

    title = sample_text.get(cert_type, "Barangay Certificate")

    if not os.path.exists("Sample_Certificates"):
        os.makedirs("Sample_Certificates")

    filename = f"Sample_Certificates/Sample_{title.replace(' ', '_')}.pdf"
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "Republic of the Philippines")
    c.drawCentredString(width / 2, height - 80, title)

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 130, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    c.drawString(100, height - 160, "Resident Name: __________________________")
    c.drawString(100, height - 180, "Address: _________________________________")

    if cert_type == "barangay_clearance":
        lines = [
            "This is to certify that the above-named individual is a resident of our barangay.",
            "They have no pending legal complaints or obligations.",
            "This certificate is issued for valid legal purposes."
        ]
    elif cert_type == "indigency":
        lines = [
            "This certifies that the individual named above is a bonafide resident of the barangay",
            "and is considered indigent based on barangay records.",
            "This certificate is issued upon request for legal purposes."
        ]
    elif cert_type == "residency":
        lines = [
            "This certifies that the individual named above is a resident of this barangay",
            "and has been living in the community for a significant duration.",
            "Issued for documentary and official purposes."
        ]
    else:
        lines = ["This is a sample certificate."]

    y = height - 220
    for line in lines:
        c.drawString(100, y, line)
        y -= 20

    c.drawString(100, y - 40, "Barangay Captain: ________________________")
    c.save()
    print(f"Generated: {filename}")

from fpdf import FPDF
from datetime import datetime
from tkinter import filedialog, messagebox
import os
import platform

def open_file(filepath):
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":
        os.system(f"open '{filepath}'")
    else:
        os.system(f"xdg-open '{filepath}'")

def generate_certificate(data):
    resident = data['resident']
    document_type = data['document_type']
    purpose = data['purpose']

    barangay = data.get('barangay', 'Sample Barangay')
    if barangay.lower().startswith("barangay "):
        barangay = barangay[9:].strip()
    barangay = f"Barangay {barangay}"

    date_str = datetime.today().strftime("%B %d, %Y")

    pdf = FPDF()
    pdf.add_page()
    width, height = 210, 297

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Republic of the Philippines", ln=True, align="C")
    pdf.cell(0, 10, barangay, ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, document_type.upper(), ln=True, align="C")
    pdf.ln(20)

    pdf.set_font("Arial", "", 12)

    if document_type == "Barangay Clearance":
        lines = [
            f"This is to certify that {resident} is a bonafide resident of {barangay}.",
            "They have no derogatory record or pending case filed in this barangay.",
            f"This clearance is issued upon their request for the purpose of {purpose}.",
        ]
    elif document_type == "Certificate of Indigency":
        lines = [
            f"This is to certify that {resident} is a bonafide resident of {barangay}.",
            "They are recognized as an indigent member of the community.",
            f"This certificate is issued upon their request for the purpose of {purpose}.",
        ]
    elif document_type == "Certificate of Residency":
        lines = [
            f"This is to certify that {resident} is a bonafide resident of {barangay}.",
            "They have been residing in the barangay for a considerable time.",
            f"This certificate is issued upon their request for the purpose of {purpose}.",
        ]
    else:
        lines = [
            f"This certifies that {resident} is a resident of {barangay}.",
            f"Issued for the purpose of {purpose}."
        ]

    for line in lines:
        pdf.multi_cell(0, 10, line)
        pdf.ln(1)

    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Issued this {date_str} at {barangay}.")
    pdf.ln(30)

    pdf.cell(0, 10, "__________________________", ln=True, align="L")
    pdf.cell(0, 10, "Barangay Captain", ln=True, align="L")

    default_name = f"{resident.replace(' ', '_')}_{document_type.replace(' ', '_')}.pdf"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=default_name,
        filetypes=[("PDF files", "*.pdf")]
    )

    if file_path:
        pdf.output(file_path)
        open_file(file_path)
        messagebox.showinfo("Success", f"Certificate saved and opened:\n{file_path}")
    else:
        messagebox.showinfo("Cancelled", "Certificate generation cancelled.")

import os
import platform
from fpdf import FPDF
from tkinter import messagebox
from ttkbootstrap import Frame, Label, Button
from ttkbootstrap.constants import *
from datetime import datetime

class Certificates(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        Label(
            self,
            text="Generate Sample Certificates",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(30, 40))

        btn_frame = Frame(self)
        btn_frame.pack()

        Button(
            btn_frame,
            text="Barangay Clearance",
            width=30,
            bootstyle="dark",
            command=lambda: self.generate_sample("Barangay Clearance")
        ).pack(pady=10)

        Button(
            btn_frame,
            text="Certificate of Indigency",
            width=30,
            bootstyle="dark",
            command=lambda: self.generate_sample("Certificate of Indigency")
        ).pack(pady=10)

        Button(
            btn_frame,
            text="Certificate of Residency",
            width=30,
            bootstyle="dark",
            command=lambda: self.generate_sample("Certificate of Residency")
        ).pack(pady=10)

    def open_file(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            os.system(f"open '{path}'")
        else:
            os.system(f"xdg-open '{path}'")

    def generate_sample(self, cert_type):
        messages = {
            "Barangay Clearance": [
                "This certifies that the individual named herein has been cleared of any",
                "derogatory records or complaints filed at the barangay level.",
                "This document may be used for employment or travel purposes."
            ],
            "Certificate of Indigency": [
                "This certifies that the bearer is recognized as indigent and belongs",
                "to a low-income household residing within the barangay jurisdiction.",
                "This document may be used to claim benefits or assistance."
            ],
            "Certificate of Residency": [
                "This certifies that the individual named herein is a resident of Barangay Pogi.",
                "They have been residing in this barangay for a significant period of time.",
                "This document is issued upon their request for valid legal purposes."
            ]
        }

        if cert_type not in messages:
            messagebox.showerror("Error", f"Unknown certificate type: {cert_type}")
            return

        output_dir = "Sample_Certificates"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/Sample_{cert_type.replace(' ', '_')}.pdf"

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, cert_type, ln=True, align="C")

        pdf.ln(20)
        pdf.set_font("Arial", size=12)

        for line in messages[cert_type]:
            pdf.multi_cell(0, 10, line)
            pdf.ln(2)

        pdf.ln(10)
        pdf.cell(0, 10, f"Generated on {datetime.today().strftime('%B %d, %Y')}", ln=True)

        pdf.output(filename)
        messagebox.showinfo("Success", f"Sample certificate generated at:\n{filename}")
        self.open_file(filename)

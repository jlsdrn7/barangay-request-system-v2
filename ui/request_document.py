import sqlite3
import tkinter as tk
from ttkbootstrap import Frame, Label, Entry, Button, Combobox, StringVar, Text
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime

DB_NAME = "barangay.db"

class RequestDocument(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        self.selected_resident = StringVar()
        self.document_type = StringVar()
        self.purpose_text = StringVar()

        form_container = Frame(self)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        Label(form_container, text="Request Document", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        Label(form_container, text="Select Resident").grid(row=1, column=0, sticky=E, padx=(0, 10), pady=(0, 10))
        self.resident_box = Combobox(form_container, textvariable=self.selected_resident, width=50, state="readonly")
        self.resident_box.grid(row=1, column=1, pady=(0, 10))
        self.load_residents()

        Label(form_container, text="Document Type").grid(row=2, column=0, sticky=E, padx=(0, 10), pady=(0, 10))
        Combobox(form_container, textvariable=self.document_type,
                 values=["Barangay Clearance", "Certificate of Indigency", "Certificate of Residency"],
                 width=50, state="readonly").grid(row=2, column=1, pady=(0, 10))

        Label(form_container, text="Purpose").grid(row=3, column=0, sticky=NE, padx=(0, 10), pady=(0, 10))
        self.purpose_entry = Text(form_container, width=50, height=4)
        self.purpose_entry.grid(row=3, column=1, pady=(0, 10))

        Button(form_container, text="Submit Request", bootstyle="primary", command=self.submit_request).grid(
            row=4, column=1, sticky=E, pady=(10, 0))

    def load_residents(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name FROM residents")
        data = cursor.fetchall()
        conn.close()
        self.residents = {f"{name} (ID: {rid})": rid for rid, name in data}
        self.resident_box["values"] = list(self.residents.keys())

    def submit_request(self):
        resident_display = self.selected_resident.get()
        doc_type = self.document_type.get()
        purpose = self.purpose_entry.get("1.0", "end").strip()

        if not resident_display or not doc_type or not purpose:
            messagebox.showerror("Missing Data", "Please fill out all fields.")
            return

        resident_id = self.residents[resident_display]
        request_date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO requests (resident_id, document_type, purpose, request_date)
            VALUES (?, ?, ?, ?)
        """, (resident_id, doc_type, purpose, request_date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Document request submitted.")
        self.selected_resident.set("")
        self.document_type.set("")
        self.purpose_entry.delete("1.0", "end")

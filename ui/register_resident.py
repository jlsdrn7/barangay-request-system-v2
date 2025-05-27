import tkinter as tk
from ttkbootstrap import Frame, Label, Entry, Button, StringVar
from ttkbootstrap.constants import *
import sqlite3

DB_NAME = "barangay.db"

class RegisterResident(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        self.name_var = StringVar()
        self.age_var = StringVar()
        self.address_var = StringVar()
        self.contact_var = StringVar()
        self.status_var = StringVar()

        # Container to center the form
        form_container = Frame(self)
        form_container.place(relx=0.5, rely=0.5, anchor="center")

        Label(form_container, text="Register New Resident", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        def add_field(label_text, var, row):
            Label(form_container, text=label_text).grid(row=row, column=0, sticky=E, pady=5, padx=(0, 10))
            Entry(form_container, textvariable=var, width=40).grid(row=row, column=1, pady=5)

        add_field("Full Name", self.name_var, 1)
        add_field("Age", self.age_var, 2)
        add_field("Address", self.address_var, 3)
        add_field("Contact Number", self.contact_var, 4)

        Button(form_container, text="Save", bootstyle="success", command=self.save_resident).grid(row=5, column=1, sticky=E, pady=(10, 0))
        Label(form_container, textvariable=self.status_var, foreground="green").grid(row=6, column=1, sticky=W)

    def save_resident(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        address = self.address_var.get().strip()
        contact = self.contact_var.get().strip()

        if not name or not age or not address or not contact:
            self.status_var.set("Please fill out all fields.")
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO residents (full_name, age, address, contact)
                VALUES (?, ?, ?, ?)
            """, (name, age, address, contact))
            conn.commit()
            conn.close()
            self.status_var.set("Resident saved successfully.")
            self.clear_form()
        except Exception as e:
            self.status_var.set(f"Error: {e}")

    def clear_form(self):
        self.name_var.set("")
        self.age_var.set("")
        self.address_var.set("")
        self.contact_var.set("")

import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
from ttkbootstrap import Frame, Label, Button, Entry, Scrollbar, StringVar
from ttkbootstrap.constants import *
from tkinter import ttk

DB_NAME = "barangay.db"

class ManageResidents(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        Label(self, text="Total Registered Residents", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(0, 10))

        search_frame = Frame(self)
        search_frame.pack(anchor=NW, pady=(0, 10))

        self.search_var = StringVar()
        Entry(search_frame, textvariable=self.search_var, width=40).pack(side=LEFT)
        Button(search_frame, text="Search", bootstyle="primary", command=self.search).pack(side=LEFT, padx=5)
        Button(search_frame, text="Clear", bootstyle="secondary", command=self.load_data).pack(side=LEFT)

        table_frame = Frame(self)
        table_frame.pack(fill=BOTH, expand=YES)

        columns = ("id", "name", "age", "address", "contact")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor=W)
        self.tree.column("id", width=30)

        vsb = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)

        btn_frame = Frame(self)
        btn_frame.pack(anchor=NW, pady=10)

        Button(btn_frame, text="Add", bootstyle="success", command=self.add).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Edit", bootstyle="warning", command=self.edit).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Delete", bootstyle="danger", command=self.delete).pack(side=LEFT, padx=5)

        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, age, address, contact FROM residents ORDER BY id DESC")
        for row in cursor.fetchall():
            self.tree.insert("", END, values=row)
        conn.close()

    def search(self):
        keyword = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, age, address, contact FROM residents")
        for row in cursor.fetchall():
            if keyword in row[1].lower():
                self.tree.insert("", END, values=row)
        conn.close()

    def add(self):
        self.open_form()

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a resident to edit.")
            return
        values = self.tree.item(selected[0], "values")
        self.open_form(values)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a resident to delete.")
            return

        resident_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this resident?")
        if confirm:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM residents WHERE id = ?", (resident_id,))
            conn.commit()
            conn.close()
            self.load_data()

    def open_form(self, data=None):
        form = tk.Toplevel(self)
        form.title("Resident Form")
        form.geometry("400x350")
        form.grab_set()

        name_var = StringVar(value=data[1] if data else "")
        age_var = StringVar(value=data[2] if data else "")
        address_var = StringVar(value=data[3] if data else "")
        contact_var = StringVar(value=data[4] if data else "")

        tk.Label(form, text="Full Name").pack(pady=(10, 0))
        tk.Entry(form, textvariable=name_var, width=40).pack()

        tk.Label(form, text="Age").pack(pady=(10, 0))
        tk.Entry(form, textvariable=age_var, width=40).pack()

        tk.Label(form, text="Address").pack(pady=(10, 0))
        tk.Entry(form, textvariable=address_var, width=40).pack()

        tk.Label(form, text="Contact").pack(pady=(10, 0))
        tk.Entry(form, textvariable=contact_var, width=40).pack()

        def save():
            name = name_var.get().strip()
            age = age_var.get().strip()
            address = address_var.get().strip()
            contact = contact_var.get().strip()

            if not name or not age or not address or not contact:
                messagebox.showerror("Error", "All fields are required.")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            if data:
                cursor.execute("""
                    UPDATE residents
                    SET full_name = ?, age = ?, address = ?, contact = ?
                    WHERE id = ?
                """, (name, age, address, contact, data[0]))
            else:
                cursor.execute("""
                    INSERT INTO residents (full_name, age, address, contact)
                    VALUES (?, ?, ?, ?)
                """, (name, age, address, contact))
            conn.commit()
            conn.close()
            form.destroy()
            self.load_data()

        Button(form, text="Save", bootstyle="primary", command=save).pack(pady=20)

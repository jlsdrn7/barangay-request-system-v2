import sqlite3
import csv
from tkinter import messagebox, filedialog
from ttkbootstrap import Frame, Label, Button, Scrollbar, Entry, StringVar
from ttkbootstrap.constants import *
from tkinter import ttk

DB_NAME = "barangay.db"

class IssuedCertificates(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        Label(self, text="Certificates Issued", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(0, 10))

        search_frame = Frame(self)
        search_frame.pack(anchor=NW, pady=(0, 10))

        self.search_var = StringVar()
        Entry(search_frame, textvariable=self.search_var, width=40).pack(side=LEFT)
        Button(search_frame, text="Search", bootstyle="primary", command=self.search_data).pack(side=LEFT, padx=5)
        Button(search_frame, text="Clear", bootstyle="secondary", command=self.load_data).pack(side=LEFT)

        table_frame = Frame(self)
        table_frame.pack(fill=BOTH, expand=YES)

        columns = ("id", "resident", "document_type", "purpose", "status", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor=W)
        self.tree.column("id", width=30)

        vsb = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)

        Button(self, text="Export CSV", bootstyle="secondary-outline", command=self.export_csv).pack(anchor=NW, pady=(15, 0))

        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, res.full_name, r.document_type, r.purpose, r.status, r.request_date
            FROM requests r
            JOIN residents res ON r.resident_id = res.id
            WHERE r.status = 'Approved'
            ORDER BY r.id DESC
        """)
        for row in cursor.fetchall():
            self.tree.insert("", END, values=row)
        conn.close()

    def search_data(self):
        keyword = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, res.full_name, r.document_type, r.purpose, r.status, r.request_date
            FROM requests r
            JOIN residents res ON r.resident_id = res.id
            WHERE r.status = 'Approved'
            ORDER BY r.id DESC
        """)
        for row in cursor.fetchall():
            if keyword in row[1].lower() or keyword in row[2].lower():
                self.tree.insert("", END, values=row)
        conn.close()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Resident", "Document Type", "Purpose", "Status", "Date"])
            for row_id in self.tree.get_children():
                writer.writerow(self.tree.item(row_id)["values"])
        messagebox.showinfo("Exported", "CSV export completed successfully.")

import sqlite3
import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from ttkbootstrap import Frame, Label, Button, Scrollbar, Entry, StringVar
from ttkbootstrap.constants import *
from tkinter import ttk
from core.generate_certificate import generate_certificate

DB_NAME = "barangay.db"

class PendingRequests(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        Label(self, text="Pending Document Requests", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(0, 10))

        search_frame = Frame(self)
        search_frame.pack(anchor=NW, pady=(0, 10))

        self.search_var = StringVar()
        Entry(search_frame, textvariable=self.search_var, width=40).pack(side=LEFT)
        Button(search_frame, text="Search", bootstyle="primary", command=self.search_requests).pack(side=LEFT, padx=5)
        Button(search_frame, text="Clear", bootstyle="secondary", command=self.load_requests).pack(side=LEFT)

        table_frame = Frame(self)
        table_frame.pack(fill=BOTH, expand=YES)

        columns = ("id", "resident", "type", "purpose", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor=W, stretch=True)
        self.tree.column("id", width=30)

        vsb = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)

        button_frame = Frame(self)
        button_frame.pack(anchor=NW, pady=(15, 0))

        Button(button_frame, text="Approve", bootstyle="success", command=lambda: self.update_status("Approved")).pack(side=LEFT, padx=5)
        Button(button_frame, text="Reject", bootstyle="danger", command=lambda: self.update_status("Rejected")).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edit", bootstyle="warning", command=self.edit_request).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", bootstyle="danger-outline", command=self.delete_request).pack(side=LEFT, padx=5)
        Button(button_frame, text="Export CSV", bootstyle="secondary-outline", command=self.export_csv).pack(side=LEFT, padx=5)
        Button(button_frame, text="Print Certificate", bootstyle="info", command=self.print_certificate).pack(side=LEFT, padx=5)

        self.load_requests()

    def load_requests(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, res.full_name, r.document_type, r.purpose, r.status
            FROM requests r
            JOIN residents res ON r.resident_id = res.id
            WHERE r.status = 'Pending'
            ORDER BY r.id DESC
        """)
        for row in cursor.fetchall():
            self.tree.insert("", END, values=row)
        conn.close()

    def search_requests(self):
        keyword = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, res.full_name, r.document_type, r.purpose, r.status
            FROM requests r
            JOIN residents res ON r.resident_id = res.id
            WHERE r.status = 'Pending'
            ORDER BY r.id DESC
        """)
        for row in cursor.fetchall():
            if keyword in row[1].lower() or keyword in row[2].lower():
                self.tree.insert("", END, values=row)
        conn.close()

    def update_status(self, new_status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a request.")
            return

        request_id = self.tree.item(selected[0], "values")[0]
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE requests SET status = ? WHERE id = ?", (new_status, request_id))
        conn.commit()
        conn.close()
        self.load_requests()

    def edit_request(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a request to edit.")
            return

        values = self.tree.item(selected[0], "values")
        request_id, _, old_type, old_purpose, _ = values

        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Request")
        edit_win.geometry("400x320")
        edit_win.grab_set()

        tk.Label(edit_win, text="Document Type").pack(pady=(10, 0))
        doc_var = tk.StringVar(value=old_type)
        doc_dropdown = ttk.Combobox(edit_win, textvariable=doc_var, state="readonly", width=37)
        doc_dropdown["values"] = ["Barangay Clearance", "Certificate of Indigency", "Certificate of Residency"]
        doc_dropdown.pack()

        tk.Label(edit_win, text="Purpose").pack(pady=(10, 0))
        purpose_var = tk.StringVar(value=old_purpose)
        tk.Entry(edit_win, textvariable=purpose_var, width=40).pack()

        def save_changes():
            new_doc = doc_var.get().strip()
            new_purpose = purpose_var.get().strip()

            if not new_doc or not new_purpose:
                messagebox.showerror("Missing Fields", "All fields must be filled.")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE requests
                SET document_type = ?, purpose = ?
                WHERE id = ?
            """, (new_doc, new_purpose, request_id))
            conn.commit()
            conn.close()

            edit_win.destroy()
            self.load_requests()
            messagebox.showinfo("Updated", "Request updated successfully.")

        tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=15)

    def delete_request(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a request to delete.")
            return

        request_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this request?")
        if confirm:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM requests WHERE id = ?", (request_id,))
            conn.commit()
            conn.close()
            self.load_requests()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Resident", "Document Type", "Purpose", "Status"])
            for row_id in self.tree.get_children():
                writer.writerow(self.tree.item(row_id)["values"])

        messagebox.showinfo("Exported", "CSV export completed successfully.")

    def print_certificate(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a request to print.")
            return

        values = self.tree.item(selected[0], "values")
        request_id = values[0]
        request_data = {
            "resident": values[1],
            "document_type": values[2],
            "purpose": values[3],
            "barangay": "Barangay Pogi"
        }

        generate_certificate(request_data)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE requests SET status = 'Approved' WHERE id = ?", (request_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Status Updated", "Request has been approved after printing certificate.")
        self.load_requests()

import sqlite3
import tkinter as tk
from ttkbootstrap import Frame, Label
from ttkbootstrap.constants import *

DB_NAME = "barangay.db"

class Dashboard(Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.pack(fill=BOTH, expand=YES)

        Label(self, text="Dashboard", font=("Segoe UI", 16, "bold")).pack(anchor=NW, pady=(0, 20))

        self.card_container = Frame(self)
        self.card_container.pack(fill=BOTH, expand=YES)

        total_residents = self.get_count("residents")
        pending = self.get_count("requests", "status = 'Pending'")
        approved = self.get_count("requests", "status = 'Approved'")
        rejected = self.get_count("requests", "status = 'Rejected'")

        self.create_card("Total Residents", total_residents, 0, 0, "primary")
        self.create_card("Pending Requests", pending, 0, 1, "warning")
        self.create_card("Approved Requests", approved, 1, 0, "success")
        self.create_card("Rejected Requests", rejected, 1, 1, "danger")

        for i in range(2):
            self.card_container.grid_columnconfigure(i, weight=1)
            self.card_container.grid_rowconfigure(i, weight=1)

    def create_card(self, title, value, row, col, color):
        card = Frame(self.card_container, bootstyle=f"{color}-light", padding=20)
        card.grid(row=row, column=col, padx=15, pady=15, sticky=NSEW)

        Label(card, text=title, font=("Segoe UI", 11, "bold")).pack(anchor=NW)
        Label(card, text=str(value), font=("Segoe UI", 24, "bold")).pack(anchor=NW, pady=(10, 0))

    def get_count(self, table, condition=None):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            query = f"SELECT COUNT(*) FROM {table}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"DB Error: {e}")
            return "N/A"

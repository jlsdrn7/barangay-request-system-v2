import tkinter as tk
from ttkbootstrap import Frame, Button
from ttkbootstrap.constants import *
from core.routes import (
    go_to_register,
    go_to_request,
    go_to_view,
    go_to_certificates,
    go_to_manage_residents,
    go_to_pending_requests,
    go_to_approved_requests,
    go_to_issued_certificates
)
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + 80
        y = self.widget.winfo_rooty() + 10
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        tw.attributes("-alpha", 0.95)

        frame = tk.Frame(tw, bg="#2c2f33", padx=8, pady=4, bd=0, relief="flat")
        frame.pack()

        label = tk.Label(
            frame,
            text=self.text,
            bg="#2c2f33",
            fg="white",
            font=("Segoe UI", 10),
            justify="left"
        )
        label.pack()

    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class MainMenu(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.icons = {
            "home": self.load_icon("home.png"),
            "user": self.load_icon("user.png"),
            "document": self.load_icon("document.png"),
            "clipboard": self.load_icon("clipboard.png"),
            "folder": self.load_icon("folder.png"),
            "logout": self.load_icon("logout.png")
        }

        sidebar = Frame(self, width=80, style="dark.TFrame")
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        icon_cmds = [
            (self.icons["home"], self.show_dashboard, "Home"),
            (self.icons["user"], lambda: go_to_register(self.content), "Register Resident"),
            (self.icons["document"], lambda: go_to_request(self.content), "Request Document"),
            (self.icons["clipboard"], lambda: go_to_view(self.content), "View Requests"),
            (self.icons["folder"], lambda: go_to_certificates(self.content), "Certificates"),
        ]

        for icon, cmd, tooltip_text in icon_cmds:
            btn = Button(sidebar, image=icon, bootstyle="dark", command=cmd)
            btn.pack(fill=X, expand=YES, pady=5)
            Tooltip(btn, tooltip_text)

        logout_btn = Button(
            sidebar,
            image=self.icons["logout"],
            bootstyle="secondary",
            command=self.logout
        )
        logout_btn.pack(side=BOTTOM, fill=X, pady=5)
        Tooltip(logout_btn, "Logout")

        self.content = Frame(self, padding=40)
        self.content.pack(side=LEFT, fill=BOTH, expand=YES)

        self.show_dashboard()

    def load_icon(self, filename, size=(64, 64)):
        path = resource_path(os.path.join("assets", filename))
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def show_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        wrapper = Frame(self.content)
        wrapper.pack(expand=YES)

        grid = Frame(wrapper)
        grid.pack()

        cards = [
            ("Total Residents", "View registered residents", "residents.png", lambda: go_to_manage_residents(self.content)),
            ("Pending Requests", "View pending document requests", "pending.png", lambda: go_to_pending_requests(self.content)),
            ("Approved Requests", "View approved requests", "approved.png", lambda: go_to_approved_requests(self.content)),
            ("Certificates Issued", "Access issued certificates", "certificate.png", lambda: go_to_issued_certificates(self.content)),
        ]

        for index, (title, desc, icon_file, command) in enumerate(cards):
            container = Frame(grid, width=340, height=220)
            container.grid(row=index // 2, column=index % 2, padx=30, pady=30)
            container.grid_propagate(False)

            canvas = tk.Canvas(container, width=340, height=220, highlightthickness=0, bg="#ffffff")
            canvas.pack(fill=BOTH, expand=YES)

            canvas.create_rectangle(15, 15, 325, 205, fill="#adb5bd", outline="", width=0)
            card = canvas.create_rectangle(0, 0, 310, 190, fill="#ffffff", outline="#dee2e6", width=1)

            frame = tk.Frame(canvas, bg="#ffffff")
            frame.place(x=10, y=10, width=300, height=180)

            icon = self.load_icon(icon_file)
            tk.Label(frame, image=icon, bg="#ffffff").pack(anchor="center", pady=(0, 10))
            tk.Label(frame, text=title, font=("Segoe UI", 16, "bold"), fg="#212529", bg="#ffffff").pack(anchor="center")
            tk.Label(frame, text=desc, font=("Segoe UI", 12), fg="#6c757d", bg="#ffffff").pack(anchor="center", pady=(5, 0))

            frame.image = icon

            for widget in (canvas, frame):
                widget.bind("<Button-1>", lambda e, cmd=command: cmd())
                widget.configure(cursor="hand2")

            for child in frame.winfo_children():
                child.bind("<Button-1>", lambda e, cmd=command: cmd())
                child.configure(cursor="hand2")

    def logout(self):
        self.master.destroy()

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ui.main_menu import MainMenu
from database import init_db

def main():
    init_db()

    app = tb.Window(themename="flatly")
    app.title("Barangay Request System v2")
    app.geometry("1000x600")
    app.resizable(False, False)

    main_menu = MainMenu(app)
    main_menu.pack(fill=BOTH, expand=YES)

    app.mainloop()

if __name__ == "__main__":
    main()

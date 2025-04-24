
import os
import customtkinter as ctk
from controllers.setup_controller import SetupController
from controllers.sales_controller import SalesController
from a_consts import CONSTS
from PIL import Image, ImageTk
from tkinter import PhotoImage


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    root = ctk.CTk()
    root.title(CONSTS.APP_NAME)
    root.iconbitmap("sporkyicon.ico")
    # Determine initial window size based on existing data
    if os.path.exists(CONSTS.BARBER_TXT):
        root.geometry("800x400+500+200")  # Larger size for sales UI
        root.resizable(True, True)
        # Load existing barbers
        with open(CONSTS.BARBER_TXT, "r", encoding="utf-8") as f:
            barbers = [line.strip() for line in f if line.strip()]
        SalesController(root, barbers)
    else:
        # First run: go through setup
        root.geometry("570x320+500+200")  # Compact size for setup UI
        root.resizable(False, False)
        SetupController(root)

    root.mainloop()


import customtkinter as ctk
from controllers.setup_controller import SetupController

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    # Single CTk root window
    root = ctk.CTk()
    root.title("Barber Shop Sales App")
    root.geometry("570x320+500+200")
    root.resizable(False, False)

    # Start with setup controller
    SetupController(root)
    root.mainloop()

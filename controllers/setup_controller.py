from views.setup_view import SetupView
from controllers.sales_controller import SalesController
from tkinter import messagebox
from a_consts import CONSTS
import os , json
import sys

class SetupController:
    def __init__(self, root):
        self.root = root
        # Display setup frame
        self.frame = SetupView(root, self.proceed)
        self.frame.pack(fill="both", expand=True)

    def proceed(self, barber_names):
        import json
        from tkinter import messagebox
        from a_consts import CONSTS
        import os, sys

        # Persist barber data
        try:
            with open(CONSTS.BARBER_TXT, "w", encoding="utf-8") as f:
                f.write("\n".join(barber_names))
            with open(CONSTS.ALL_JSON, "w", encoding="utf-8") as f:
                json.dump(barber_names, f, indent=2)
            # Create each barber JSON if missing
            for name in barber_names:
                path = CONSTS.BARBER_JSON_TMPL.format(name)
                if not os.path.exists(path):
                    with open(path, "w", encoding="utf-8") as bf:
                        json.dump([], bf)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save barber data: {e}")
            return

        messagebox.showinfo("Success", "Barber(s) created successfully—launching sales UI.")
        # Tear down setup UI
        self.frame.pack_forget()
        # Resize and launch sales
        self.root.geometry("900x550+520+80")  
        self.root.resizable(True, True)
        self.root.minsize(750, 320)
        SalesController(self.root, barber_names)




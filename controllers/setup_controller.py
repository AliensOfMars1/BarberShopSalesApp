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

    def proceed(self):
        print("SetupController.proceed called", file=sys.stdout, flush=True)
        barber_input = self.frame.get_barber_name().strip()
        barber_names = [name.strip() for name in barber_input.split(",") if name.strip()]
        self.barber_names = barber_names  # Store the barber names in a list
        # Debugging output
        print(f"Proceed callback invoked with: {barber_names}", file=sys.stdout, flush=True)

        # Validate input
        if not barber_names:
            messagebox.showerror("EMPTY!", "Barber name(s) cannot be empty.")
            return

        # Persist barber data
        try:
            # 1) Write barbers.txt
            with open(CONSTS.BARBER_TXT, "w", encoding="utf-8") as f:
                f.write("\n".join(barber_names))

            # 2) Write all_barbers.json
            with open(CONSTS.ALL_JSON, "w", encoding="utf-8") as f:
                json.dump(barber_names, f, indent=2)

            # 3) Create individual JSON files if not already present
            for name in barber_names:
                filename = CONSTS.BARBER_JSON_TMPL.format(name)
                if not os.path.exists(filename):
                    with open(filename, "w", encoding="utf-8") as bf:
                        json.dump([], bf)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save barber data: {e}")
            return

        # Setup complete: resize window and launch Sales UI
        messagebox.showinfo("Success", "Barber(s) created successfully—launching sales UI.")
        self.root.geometry("800x400")
        self.frame.pack_forget()
        SalesController(self.root, barber_names)

    




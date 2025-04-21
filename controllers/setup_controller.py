from views.setup_view import SetupView
from controllers.sales_controller import SalesController
from tkinter import messagebox

class SetupController:
    def __init__(self, root):
        self.root = root
        # Display setup frame
        self.frame = SetupView(root, self.proceed)
        self.frame.pack(fill="both", expand=True)


    def proceed(self):
        import sys
        print("SetupController.proceed called", file=sys.stdout, flush=True)
        barber_name = self.frame.get_barber_name().strip()
        barber_names = [name.strip() for name in barber_name.split(",")] # Split the names by comma and strip any extra spaces
        self.barber_names = barber_names # Store the barber names in a list
        print(f"Proceed callback invoked with: '{barber_names}'", file=sys.stdout, flush=True)
        # Show success message (optional)
        messagebox.showinfo("Success", "Barber names collected successfully.") 
        if not barber_name:
            # Show error if no barber name entered
            messagebox.showerror("EMPTY!", "Barber name(s) cannot be empty.")
        else:
            # Remove setup frame and initialize sales controller
            # Remove setup frame and show sales frame
            self.frame.pack_forget()
            SalesController(self.root, barber_names)







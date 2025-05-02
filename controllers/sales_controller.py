
from models.model import SalesModel
from views.sales_view import SalesView
from tkinter import messagebox
import customtkinter as ctk
from a_consts import CONSTS
import os , json, sys
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog

class SalesController:
    def __init__(self, root, barber_names):
        # Initialize model
        self.model = SalesModel()
        self.barber_names = barber_names
        self.root = root

        # Initialize view with callbacks
        self.frame = SalesView(
            root,
            barber_names,
            record_callback=self.record_sale,
            view_history_callback=self.view_history,
            reset_callback=self.reset_app
        )
        self.frame.pack(fill="both", expand=True)

    def record_sale(self, barber, service, amount):
        # Validate selections
        if not barber or barber == "Select Barber":
            self.frame.set_status("Please select a barber.", success=False)
            return
        if not service or service == "Select Service":
            self.frame.set_status("Please select a service.", success=False)
            return
        # Record sale via model
        try:
            sale = self.model.record_sale(barber, service, amount)
            self.frame.set_status(f"Recorded: {barber} - {service} -GH₵{sale['amount']:.2f}", success=True)
            self.clear_inputs()
        except ValueError:
            self.frame.set_status("Invalid amount. Please enter a number.", success=False)

              # Persist to individual barber JSON file
        try:
            filename = CONSTS.BARBER_JSON_TMPL.format(barber)
            # Read existing records
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as bf:
                    data = json.load(bf)
            else:
                data = []
            # Append new sale and save
            data.append(sale)
            with open(filename, 'w', encoding='utf-8') as bf:
                json.dump(data, bf, indent=2)
        except Exception as e:
            # Log failure but continue
            print(f"Failed to save sale to {filename}: {e}", file=sys.stderr)    

    def clear_inputs(self):
        # Reset inputs to default
        self.frame.barber_dropdown.set("Select Barber")
        self.frame.service_type.set("Select Service")
        # Clear amount entry
        self.frame.amount_entry.delete(0, "end")

    def view_history(self):
        # Display sales history
        log = self.model.get_sales_log()
        if not log:
            messagebox.showinfo("Sales History", "No sales recorded yet.")
            return
        history_lines = [
            f"{item['time']} - {item['barber']} - {item['service']} - GH₵{item['amount']:.2f}"
            for item in log
        ]
        history = "\n".join(history_lines)
        messagebox.showinfo("Sales History", history)

    def ask_admin_credentials(self):
        # Create a custom Toplevel dialog to ask for admin credentials
        dlg = tk.Toplevel(self.root)
        dlg.title("Admin Authentication")
        dlg.geometry("300x150+550+300")
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text="Username:").pack(pady=(10, 0))
        user_var = tk.StringVar()
        tk.Entry(dlg, textvariable=user_var).pack()

        tk.Label(dlg, text="Password:").pack(pady=(10, 0))
        pass_var = tk.StringVar()
        tk.Entry(dlg, textvariable=pass_var, show="*").pack()

        result = {"user": None, "pass": None}

        def on_ok():
            result["user"] = user_var.get()
            result["pass"] = pass_var.get()
            dlg.destroy()

        tk.Button(dlg, text="OK", command=on_ok).pack(pady=10)
        self.root.wait_window(dlg)
        return result["user"], result["pass"]



    def reset_app(self):

        # Prompt for admin credentials via custom dialog
        username, password = self.ask_admin_credentials()
        if not username or not password:
            return
        # Verify credentials via model
        if not self.model.verify_admin(username, password):
            messagebox.showerror("Authentication Failed", "Invalid admin credentials.")
            return

        # Confirm reset
        if not messagebox.askyesno("Confirm Reset", "This will erase all data and close the app. Continue?"):
            return

        # Delete persisted barber data
        for path in (CONSTS.BARBER_TXT, CONSTS.ALL_JSON):
            try:
                os.remove(path)
            except OSError:
                pass
        for name in self.barber_names:
            try:
                os.remove(CONSTS.BARBER_JSON_TMPL.format(name))
            except OSError:
                pass

        # Clear in-memory sales log
        self.model.sales_log.clear()

        # Close the application immediately
        self.frame.destroy()
        self.root.destroy()


    def update_barber_names(self, barber_names):
        # Update model and view with new barber names
        self.barber_names = barber_names
        self.frame.update_barber_names(barber_names)


    
    
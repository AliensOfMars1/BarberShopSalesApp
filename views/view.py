import customtkinter as ctk
from tkinter import messagebox

class SalesView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.title("Barbershop Sales Recorder")
        self.geometry("900x600+100+30")

        ctk.CTkLabel(self, text="Barbershop Sales", font=("Arial", 20, "bold")).pack(pady=10)

        # Initialize with a temporary value; will be updated later
        self.barber_dropdown = ctk.CTkOptionMenu(self, values=["Loading..."])
        self.barber_dropdown.pack(pady=10)

        self.customer_entry = ctk.CTkEntry(self, placeholder_text="Customer Name")
        self.customer_entry.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Sale Amount")
        self.amount_entry.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

        ctk.CTkButton(self, text="Record Sale", command=self.controller.record_sale).pack(pady=10)
        ctk.CTkButton(self, text="Admin Login", command=self.controller.open_admin_login).pack(pady=20)
        open_btn = ctk.CTkButton(self, text="Open Toplevel", command=self.open_toplevel)
        open_btn.pack(pady=20)

        # For the loading animation (if needed)
        self.loading_dots = [".", "..", "..."]
        self.loading = False
        self.loading_index = 0

        # Immediately show the Barber Setup window after the main window is ready
        self.after(0, self.show_barber_setup)

    def show_barber_setup(self):
        setup_window = ctk.CTkToplevel(self)
        setup_window.title("Setup Barbers")
        setup_window.geometry("400x300")
        setup_window.grab_set()  # Make it modal

        ctk.CTkLabel(setup_window, text="Enter Barber Names (comma separated)", font=("Arial", 14)).pack(pady=10)
        barber_entry = ctk.CTkEntry(setup_window, width=300, placeholder_text="e.g., Mike, Alex, Sasha")
        barber_entry.pack(pady=10)

        def on_proceed():
            raw_text = barber_entry.get()
            # Split by comma and remove any surrounding whitespace
            barber_list = [name.strip() for name in raw_text.split(",") if name.strip()]
            if barber_list:
                # Update the model's barber list and refresh the dropdown
                self.controller.model.barbers = barber_list
                self.barber_dropdown.configure(values=barber_list)
                self.barber_dropdown.set(barber_list[0])
                setup_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter at least one barber name.")

        ctk.CTkButton(setup_window, text="Proceed", command=on_proceed).pack(pady=20)

    def get_sale_input(self):
        return {
            "barber": self.barber_dropdown.get(),
            "customer": self.customer_entry.get(),
            "amount": self.amount_entry.get()
        }

    def clear_inputs(self):
        self.customer_entry.delete(0, ctk.END)
        self.amount_entry.delete(0, ctk.END)

    def update_status(self, message, color="green"):
        self.status_label.configure(text=message, text_color=color)

    def show_sales_log(self, sales_log):
        log_window = ctk.CTkToplevel(self)
        log_window.title("Sales Log")
        log_window.geometry("500x400")

        if not sales_log:
            ctk.CTkLabel(log_window, text="No sales recorded yet.").pack(pady=20)
            return

        for sale in sales_log:
            text = f"[{sale['time']}] {sale['barber']} - {sale['customer']} - ₵{sale['amount']:.2f}"
            ctk.CTkLabel(log_window, text=text, anchor="w", justify="left").pack(fill="x", padx=10)

    def show_login_window(self, login_callback):
        login_window = ctk.CTkToplevel(self)
        login_window.title("Admin Login")
        login_window.geometry("300x200")

        ctk.CTkLabel(login_window, text="Username").pack(pady=5)
        username_entry = ctk.CTkEntry(login_window)
        username_entry.pack(pady=5)

        ctk.CTkLabel(login_window, text="Password").pack(pady=5)
        password_entry = ctk.CTkEntry(login_window, show="*")
        password_entry.pack(pady=5)

        def attempt_login():
            username = username_entry.get()
            password = password_entry.get()
            login_callback(username, password, login_window)

        ctk.CTkButton(login_window, text="Login", command=attempt_login).pack(pady=10)

    def open_toplevel(self):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title("3 Divisions - Vertical")
        toplevel.geometry("400x300")

        # 3 vertically stacked frames
        frame1 = ctk.CTkFrame(toplevel, fg_color="transparent", height=100, border_width=2, border_color="#444")
        frame2 = ctk.CTkFrame(toplevel, fg_color="transparent", height=100, border_width=2, border_color="#444")
        frame3 = ctk.CTkFrame(toplevel, fg_color="transparent", height=100, border_width=2, border_color="#444")

        frame1.pack(side='left', fill='y', expand=True)
        frame2.pack(side='left', fill='y', expand=True)
        frame3.pack(side='left', fill='y', expand=True)

        ctk.CTkLabel(frame1, text=" Division 1").pack(pady=10)
        ctk.CTkLabel(frame2, text=" Division 2").pack(pady=10)
        ctk.CTkLabel(frame3, text=" Division 3").pack(pady=10)

    # Loading Animation Methods ----
    def start_loading_animation(self):
        self.loading = True
        self.loading_index = 0
        self.animate_loading()

    def animate_loading(self):
        if self.loading:
            self.update_status(f"Loading{self.loading_dots[self.loading_index]}")
            self.loading_index = (self.loading_index + 1) % len(self.loading_dots)
            self.after(500, self.animate_loading)

    def stop_loading_animation(self):
        self.loading = False

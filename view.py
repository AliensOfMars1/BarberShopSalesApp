import customtkinter as ctk
from tkinter import messagebox

class SalesView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.title("Barbershop Sales Recorder")
        self.geometry("900x600+100+30")

        ctk.CTkLabel(self, text="Barbershop Sales", font=("Arial", 20, "bold")).pack(pady=10)

        self.barber_dropdown = ctk.CTkOptionMenu(self, values=controller.get_barbers())
        self.barber_dropdown.set(controller.get_barbers()[0])
        self.barber_dropdown.pack(pady=10)

        self.customer_entry = ctk.CTkEntry(self, placeholder_text="Customer Name")
        self.customer_entry.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Sale Amount")
        self.amount_entry.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

        ctk.CTkButton(self, text="Record Sale", command=self.controller.record_sale).pack(pady=10)
        ctk.CTkButton(self, text="Admin Login", command=self.controller.open_admin_login).pack(pady=20)

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

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()  # Get current mode ("Light" or "Dark" or "System")
        # Toggle to the opposite theme (ignoring "System" for simplicity)
        if current_mode == "Dark":
            new_mode = "Light"
        else:
            new_mode = "Dark"
        ctk.set_appearance_mode(new_mode)
        messagebox.showinfo("THEME",f"Theme switched to {new_mode} Mode")      

    # Loading Animation Methods ----
    def start_loading_animation(self):
        self.loading = True
        self.loading_index = 0
        self.animate_loading()

    def animate_loading(self):
        if self.loading:
            self.update_display(f"Loading{self.loading_dots[self.loading_index]}")
            self.loading_index = (self.loading_index + 1) % len(self.loading_dots)
            self.after(500, self.animate_loading)

    def stop_loading_animation(self):
        self.loading = False                

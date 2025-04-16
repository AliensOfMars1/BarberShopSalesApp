from models.model import SalesModel
from views.view import SalesView
import customtkinter as ctk

class SalesController:
    def __init__(self):
        self.model = SalesModel()
        self.view = SalesView(self)
        self.view.mainloop()

    def get_barbers(self):
        return self.model.barbers

    def record_sale(self):
        data = self.view.get_sale_input()
        if not data["customer"] or not data["amount"]:
            self.view.update_status("Please fill all fields.", "red")
            return

        try:
            sale_amount = float(data["amount"])
        except ValueError:
            self.view.update_status("Amount must be a number.", "red")
            return

        self.model.record_sale(data["barber"], data["customer"], sale_amount)
        self.view.update_status(f"Sale recorded for {data['customer']}.", "green")
        self.view.clear_inputs()

    def open_admin_login(self):
        self.view.show_login_window(self.login_admin)

    def login_admin(self, username, password, login_window):
        if self.model.verify_admin(username, password):
            login_window.destroy()
            self.view.show_sales_log(self.model.get_sales_log())
        else:
            # Update (or create) error label for failed login
            error_label = getattr(login_window, 'error_label', None)
            if error_label is None:
                error_label = ctk.CTkLabel(login_window, text="Invalid credentials", text_color="red")
                error_label.pack(pady=5)
                setattr(login_window, 'error_label', error_label)
            else:
                error_label.configure(text="Invalid credentials")

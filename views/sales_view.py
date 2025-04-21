# ============ views/sales_view.py ============
import customtkinter as ctk

class SalesView(ctk.CTkFrame):
    def __init__(self, master, barber_names):
        super().__init__(master)
        self.configure(fg_color="#222222")

        # Welcome label
        label = ctk.CTkLabel(
            self,
            text=f"Barbers: {barber_names}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        label.pack(pady=20)


        # TODO: build out the rest of the sales UI here
        # e.g., buttons for adding sales, viewing history, etc.
        

        self.barber_dropdown = ctk.CTkOptionMenu(self, values=["Loading..."])
        self.barber_dropdown.set("Select Barber")
        self.barber_dropdown.pack(pady=10)
        update_barber_names = lambda names: self.barber_dropdown.configure(values=names)
        update_barber_names(barber_names)

        self.service_type = ctk.CTkOptionMenu(self, values=["Simple Adult Cut", "Shave", "Beard Trim", "Kids cut","Hair Wash", "haircut & Dye"])
        self.service_type.set("Select service type")
        self.service_type.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Sale Amount")
        self.amount_entry.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)




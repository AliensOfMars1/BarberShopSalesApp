import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os 
from PIL import Image, ImageTk

class SalesView(ctk.CTkFrame):
    def __init__(self, master, barber_names, record_callback,reset_callback, view_history_callback=None, export_callback = None):
        
        super().__init__(master)
        self.configure(fg_color="#222222")
        self.record_callback = record_callback
        self.view_history_callback = view_history_callback
        self.reset_callback = reset_callback
        self.export_callback = export_callback # Placeholder for export callback

                # Background image overlay
        bg_path = os.path.join(os.path.dirname(__file__), "sales_view_bg.jpg") # "sales_view_bg.jpg"
        if os.path.exists(bg_path):
            img = Image.open(bg_path)
            self.bg_image = ImageTk.PhotoImage(img)
            bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
  
        #Title label
        title = ctk.CTkLabel(
            self, text="SALES RECORDER", font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white", width=200, fg_color="#4169E1", corner_radius=0
        )
        title.place(relx=0.75, rely=0.1, anchor="center")

        # Barber dropdown
        self.barber_dropdown = ctk.CTkOptionMenu(self, values=barber_names, corner_radius=0)
        self.barber_dropdown.set("Select Barber")
        self.barber_dropdown.place(relx=0.75, rely=0.2, anchor="center")

        #Service dropdown
        self.service_type = ctk.CTkOptionMenu(
            self, values=["Simple Adult Cut", "Shave", "Beard Trim", "Kids Cut", "Hair Wash", "Haircut & Dye"],
            corner_radius=0
        )
        self.service_type.set("Select Service")
        self.service_type.place(relx=0.75, rely=0.3, anchor="center")

        # MIKE, JAMES, JOE, SAM, TOM, BOB

        # Amount entry
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="e.g., 25.00", corner_radius=0)
        self.amount_entry.place(relx=0.75, rely=0.4, anchor="center")

        # Record Sale button
        self.record_btn = ctk.CTkButton(
            self, text="RECORD SALE", command=self.on_record_sale,
            font=ctk.CTkFont(size=16, weight="bold"), corner_radius=0, width=150, height=40,
            fg_color="#4CAF50", hover_color="#45a049", text_color="white"
        )
        self.record_btn.place(relx=0.75, rely=0.55, anchor="center")


        # View History button (optional)
        if self.view_history_callback:
            self.history_btn = ctk.CTkButton(
                self, corner_radius=0,
                text="View History",
                command=self.view_history_callback
            )
            self.history_btn.place(relx=0.75, rely=0.75, anchor="center")

        # Status label
        self.status_label = ctk.CTkLabel(self, text="", text_color="white")
        self.status_label.place(relx=0.75, rely=0.65, anchor="center")

                # Reset Button
        self.reset_btn = ctk.CTkButton(
            self,
            text="Reset All",
            command=self.reset_callback,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#880000",
            hover_color="#aa0000", width= 30, corner_radius=0
        )
        self.reset_btn.place(relx=0.1, rely=0.95, anchor="se")

       #Export Button
        self.export_btn = ctk.CTkButton(
            self,
            text="Export Sales",
            command=self.export_callback,
            font=ctk.CTkFont(size=14, weight="bold"),
            width= 30, corner_radius=0
        )
        self.export_btn.place(relx=0.95, rely=0.95, anchor="se")
   

    def on_record_sale(self):
        barber = self.barber_dropdown.get()
        service = self.service_type.get()
        amount = self.amount_entry.get().strip()
        self.record_callback(barber, service, amount)

    def set_status(self, message, success=True):
        color = "green" if success else "red"
        self.status_label.configure(text=message, text_color=color)
            # Schedule to clear the message after 'duration' milliseconds
        self.after(2000, lambda: self.status_label.configure(text=""))

    def update_barber_names(self, barber_names):
        self.barber_dropdown.configure(values=barber_names)
        self.barber_dropdown.set("Select Barber")

        
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os 
from PIL import Image, ImageTk
import json
from a_consts import CONSTS
from datetime import datetime


class SalesView(ctk.CTkFrame):
    def __init__(self, master, barber_names, record_callback,reset_callback, view_history_callback=None, export_callback = None):
        
        super().__init__(master)
        self.configure(fg_color="#222222")
        self.record_callback = record_callback
        self.view_history_callback = view_history_callback
        self.reset_callback = reset_callback
        self.export_callback = export_callback # Placeholder for export callback
        self.barber_names = barber_names



        # Load the original image once
        bg_path = os.path.join(os.path.dirname(__file__), "view_images", "Mirage_view_bg.jpg")
        if os.path.exists(bg_path):
            self.original_bg_image = Image.open(bg_path)
            self.bg_label = ctk.CTkLabel(self, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            def update_background(event=None):
                width = self.winfo_width()
                height = self.winfo_height()
                resized = self.original_bg_image.resize((width, height), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(resized)
                self.bg_label.configure(image=self.bg_image)

            # Call once initially, then bind to window resize
            update_background()
            self.bind("<Configure>", update_background)
  
                #Title label
        title = ctk.CTkLabel(
            self, text="SALES RECORDER", font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white", width=300, fg_color="#1A1F2B", corner_radius=0
        )
        title.place(relx=0.75, rely=0.1, anchor="center")

#___________________________sidebar_____________________________________________________

        #Sidebar Base with Shadow
        shadow = ctk.CTkFrame(self, width=250, fg_color="#0f131b", corner_radius=0)
        shadow.place(x=0, y=0, relheight=1)
        self.sidebar = ctk.CTkFrame(self, fg_color="#1A1F2B", corner_radius=0)
        self.sidebar.place(x=5, y=4, relheight=0.98)

        # Logo / Header
        logo = ctk.CTkLabel(self.sidebar, text="🧔 BarberApp",
            font=ctk.CTkFont(size=18, weight="bold"), pady=20)
        logo.pack()

        # Separator
        sep = ttk.Separator(self.sidebar, orient="horizontal")
        sep.pack(fill="x", pady=(0,10), padx=20)

        # Buttons
        for text, color in [("History","#E0E0E0"), ("Export","#F1C40F"), ("Reset","#E74C3C"),("View Sales","#5DADE2")]:
            cammand = None
            if text == "History":
                cammand = lambda: self.view_history_callback() if self.view_history_callback else None
            elif text == "Export":
                cammand = lambda: self.export_callback() if self.export_callback else None
            elif text == "Reset":
                cammand = lambda : self.reset_callback() if self.reset_callback else None
            elif text == "View Sales":
                cammand = lambda : self.view_sales() if self.view_sales else None                
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                fg_color=color,
                text_color="#1A1F2B" if color!="#E0E0E0" else "#1A1F2B",
                corner_radius=8,
                height=40,
                command=cammand
            )
            btn.pack(padx=20, pady=5, fill="x")

#___________________________sales_frame_____________________________________________________

        sales_frame = ctk.CTkFrame(self, width=400,height=400, fg_color="#0F1B24", corner_radius=12)
        sales_frame.place(relx=0.5, rely=0.2, relwidth=0.7, relheight=1)
        # sales_frame.place(relx=0.75, rely=0.2, anchor="center")


                # Barber dropdown in sales_frame
        self.barber_dropdown = ctk.CTkOptionMenu(
            sales_frame,  # <- Important change
            values=barber_names,
            corner_radius=12,  # Rounded corners
            fg_color="#1A1F2B",  # Background color of the dropdown
            width=300,  # Wider width for better look
            height= 40
        )
        self.barber_dropdown.set("Select Barber")
        self.barber_dropdown.place(relx=0.4, rely=0.1, anchor="center")

                #Service dropdown
        self.service_type = ctk.CTkOptionMenu(
            sales_frame, values=["Simple Adult Cut", "Shave", "Beard Trim", "Kids Cut", "Hair Wash", "Haircut & Dye"],
            fg_color="#1A1F2B",  # Background color of the dropdown
            corner_radius=12, width=300,height=30  # Wider width for better look
        )
        self.service_type.set("Select Service")
        self.service_type.place(relx=0.4, rely=0.22, anchor="center")  # Centered in the frame

        # MIKE, JAMES, JOE, SAM, TOM, BOB

        # Amount entry
        self.amount_entry = ctk.CTkEntry(sales_frame, placeholder_text="e.g., 25.00", corner_radius=12, width=200)
        self.amount_entry.place(relx=0.4, rely=0.34, anchor="center")
      
        # Status label
        self.status_label = ctk.CTkLabel(sales_frame, text="", text_color="white")
        self.status_label.place(relx=0.4, rely=0.42, anchor="center")

        # Record Sale button
        self.record_btn = ctk.CTkButton(
            sales_frame, text="RECORD SALE", command=self.on_record_sale,
            font=ctk.CTkFont(size=16, weight="bold"), corner_radius=20, width=150, height=50,
            fg_color="#4CAF50", hover_color="#45a049", text_color="white"
        )
        self.record_btn.place(relx=0.4, rely=0.52, anchor="center")

#___________________________most_functions_____________________________________________________


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
    

    def show_help_window(self):
        # Check if the toplevel window already exists
        if hasattr(self, "help_window") and self.help_window.winfo_exists():
            self.help_window.lift() # Bring it to the front
            return  # Exit the function if the window is already open
        self.help_window = ctk.CTkToplevel()
        self.help_window.title("Help")
        self.help_window.geometry("680x550+200+40")
        # Set the window as transient so it stays on top of the main window
        self.help_window.transient(self)
        self.help_window.attributes("-topmost", True)  # Forces it to be on top
        self.help_window.lift() # Bring to front
        self.help_window.focus_force()
        # Create a scrollable textbox
        text_widget = ctk.CTkTextbox(self.help_window, width=480, height=350, wrap="word", font=("Arial", 14))
        text_widget.pack(pady=10, padx=10, fill="both", expand=True)   
                # Get the history from the model and insert it
        
        # text_widget.insert("1.0", CONSTS.HELP_TEXT )

        # text_widget.configure(state="disabled") # Make the text read-only      




    def view_sales(self):

        # — Prevent multiple windows and ensure front focus —
        if hasattr(self, "sales_window") and self.sales_window.winfo_exists():
            self.sales_window.lift()
            self.sales_window.focus_force()
            return

        # 1) Load each barber’s records
        sales_by_barber = {}
        for name in self.barber_names:
            path = CONSTS.BARBER_JSON_TMPL.format(name)
            if not os.path.exists(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except Exception:
                continue
            if records:
                sales_by_barber[name] = records

        # 2) Build display lines
        lines = []
        def sort_key(date_str):
            try:
                return (0, datetime.strptime(date_str, "%A, %d/%m/%Y"))
            except Exception:
                return (1, date_str)

        for barber, recs in sorted(sales_by_barber.items()):
            lines.append(f"___________________________\n\n{barber}\n___________________________")
            lines.append("")  # Blank line for spacing
            lines.append("Sales:")  # Heading
            lines.append("")  # Blank line for spacing

            # Group by date (converted to A, DD/MM/YYYY)
            by_date = {}
            for r in recs:
                raw = r.get("date") or r.get("time") or ""
                date_key = "Unknown Date"
                if raw:
                    if " " in raw:
                        try:
                            dt = datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
                            date_key = dt.strftime("%A, %d/%m/%Y")
                        except Exception:
                            part = raw.split(" ")[0]
                            try:
                                dt2 = datetime.strptime(part, "%Y-%m-%d")
                                date_key = dt2.strftime("%A, %d/%m/%Y")
                            except Exception:
                                date_key = part
                    else:
                        try:
                            dt = datetime.fromisoformat(raw)
                            date_key = dt.strftime("%A, %d/%m/%Y")
                        except Exception:
                            date_key = raw
                by_date.setdefault(date_key, []).append(r)

            overall_total = 0.0

            # 3) For each date, in order
            for date_str in sorted(by_date.keys(), key=sort_key):
                items = by_date[date_str]

                # Date heading
                lines.append(date_str)
                lines.append("")

                # List each sale
                daily_total = 0.0
                for r in items:
                    svc = r.get("service", "<no service>")
                    amt = float(r.get("amount", 0))
                    daily_total += amt
                    lines.append(f"  • {svc}: ₵{amt:.2f}")

                # Blank line before the sub‑total
                lines.append("")

                # Daily subtotal
                lines.append(f"  Daily Sub‑total: ₵{daily_total:.2f}")
                lines.append("")  # blank line to separate next date

                overall_total += daily_total

            # 4) Overall total & commission
            lines.append(f"Total Sales: ₵{overall_total:.2f}")
            commission = overall_total / 3.0
            lines.append(f"Barber’s Commission (⅓): ₵{commission:.2f}")
            lines.append("")  # blank line between barbers

        summary = "\n".join(lines) or "No sales data found."

        # 5) Show in a scrollable toplevel window
        self.sales_window = ctk.CTkToplevel(self)
        win = self.sales_window
        win.title("All Sales by Barber")
        win.geometry("500x600")

        # Keep it on top of the main application window
        win.transient(self.master)
        win.attributes("-topmost", True)
        win.focus_force()

        box = ctk.CTkTextbox(win, width=480, height=560, wrap="word")
        box.pack(padx=10, pady=10, fill="both", expand=True)
        box.insert("1.0", summary)
        box.configure(state="disabled")


import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os 
from PIL import Image, ImageTk
from a_consts import CONSTS
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from tkinter import filedialog
import os, json
from tkinter import messagebox, simpledialog
from customtkinter import CTkImage
from PIL import Image



class SalesView(ctk.CTkFrame):
    def __init__(self, master, barber_names, record_callback, reset_callback,
                  view_history_callback=None, export_callback = None, 
                  view_expenses_callback=None, view_sales_callback=None):
        """
        Initialize the SalesView with a master window and callbacks for actions. """
        
        super().__init__(master)
        self.configure(fg_color="#222222")
        self.record_callback = record_callback
        self.view_history_callback = view_history_callback
        self.reset_callback = reset_callback
        self.export_callback = export_callback # Placeholder for export callback
        self.barber_names = barber_names
        self.view_expenses_callback = view_expenses_callback # Placeholder for view expenses callback
        self.view_sales_callback = view_sales_callback # Placeholder for view sales callback



        # Load the original image once
        bg_path = os.path.join(os.path.dirname(__file__), "view_images","background", "Mirage_view_bg.jpg") #"Mirage_view_bg.jpg", "app_bg.jpg"
        if os.path.exists(bg_path):
            # 1) Load and keep the PIL image
            self.original_bg_pil = Image.open(bg_path)
            # 2) Create an initial CTkImage sized to the current window
            init_w, init_h = self.winfo_width() or 800, self.winfo_height() or 400
            self.bg_ctk_image = CTkImage(self.original_bg_pil, size=(init_w, init_h))
            # 3) Place it
            self.bg_label = ctk.CTkLabel(self, image=self.bg_ctk_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            # 4) Define a resize callback
            def update_background(event=None):
                w, h = self.winfo_width(), self.winfo_height()
                # Resize the PIL image
                resized_pil = self.original_bg_pil.resize((w, h), Image.Resampling.LANCZOS)
                # Wrap it in a new CTkImage
                self.bg_ctk_image = CTkImage(resized_pil, size=(w, h))
                # Update the label
                self.bg_label.configure(image=self.bg_ctk_image)

            # 5) Bind it and call once
            update_background()
            self.bind("<Configure>", update_background)

                #Title label
        title = ctk.CTkLabel(
            self, text="SALES RECORDER", font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white", width=300, fg_color="#1A1F2B", corner_radius=0
        )
        title.place(relx=0.75, rely=0.1, anchor="center")

        #____________________________________________________________________________sidebar

        #Sidebar Base with Shadow
        shadow = ctk.CTkFrame(self, width=210, fg_color="#0f131b", corner_radius=0)
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

        # Load icons
        icon_dir = os.path.join(os.path.dirname(__file__), "view_images", "icons")
        icons = {
            "History": CTkImage(Image.open(os.path.join(icon_dir, "history_icon.png")), size=(24, 24)),
            "Export": CTkImage(Image.open(os.path.join(icon_dir, "export.png")), size=(24, 24)),
            "Reset App": CTkImage(Image.open(os.path.join(icon_dir, "reset.png")), size=(24, 24)),
            "View Sales": CTkImage(Image.open(os.path.join(icon_dir, "sales.png")), size=(24, 24)),
            "View Expense": CTkImage(Image.open(os.path.join(icon_dir, "expense.png")), size=(24, 24)),
        }
        # Buttons
        for text, color in [("History","#E0E0E0"), ("Export","#F1C40F"), ("Reset App","#E74C3C"),
                            ("View Sales","#5DADE2"), ("View Expense","#1ABC9C")]:
            cammand = None
            if text == "History":
                cammand = lambda: self.view_history_callback() if self.view_history_callback else None
            elif text == "Export":
                cammand = lambda: self.export_callback() if self.export_callback else None
            elif text == "Reset App":
                cammand = lambda : self.reset_callback() if self.reset_callback else None
            elif text == "View Sales":
                cammand = lambda : self.view_sales_callback() if self.view_sales_callback else None      
            elif text == "View Expense":
                cammand = lambda : self.view_expenses_callback() if self.view_expenses_callback else None

            # Create button with rounded corners and shadow effect        
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                image=icons.get(text),
                compound="left",
                fg_color=color,
                text_color="#1A1F2B" if color!="#E0E0E0" else "#1A1F2B",
                corner_radius=8,
                height=40,
                command=cammand
            )
            btn.pack(padx=20, pady=5, fill="x")


        # ─── Admin Button at bottom ────────────────────────────────
        # load icon
        icon_path = os.path.join(os.path.dirname(__file__),
                                "view_images", "icons",
                                "admin_icon_white.png")
        if os.path.exists(icon_path):
            admin_icon = CTkImage(Image.open(icon_path), size=(24,24))
        else:
            admin_icon = None

        # create a button with the icon and text

        # admin button with the icon
        admin_btn = ctk.CTkButton(
            self.sidebar,
            text="Admin",
            image=admin_icon,
            compound="left",
            fg_color="#34495E",
            text_color="white",
            corner_radius=8,
            height=40,
            command=self.open_admin_panel
        )
        admin_btn.pack(padx=20, pady=20, fill="x")
        # ─────────────────────────────────────────────────────────────




#________________________________________________________________________________sales_frame

        sales_frame = ctk.CTkFrame(self, width=400,height=400, fg_color="#0F1B24", corner_radius=12)
        sales_frame.place(relx=0.5, rely=0.2, relwidth=0.7, relheight=1)
        # sales_frame.place(relx=0.75, rely=0.2, anchor="center")


                # Barber dropdown in sales_frame
        self.barber_dropdown = ctk.CTkOptionMenu(
            sales_frame,  # <- Important change
            values=barber_names,
            corner_radius=12,  # Rounded corners
            fg_color="#5DADE2",  # Background color of the dropdown
            width=300,  # Wider width for better look
            height= 40
        )
        self.barber_dropdown.set("Select Barber")
        self.barber_dropdown.place(relx=0.4, rely=0.2, anchor="center")

                # 1a) Path to the services file (sits next to expense.json)
        self.services_path = os.path.join(os.path.dirname(__file__), "..", "services.json")

        # 1b) Load or initialize with defaults
        if os.path.exists(self.services_path):
            with open(self.services_path, "r", encoding="utf-8") as f:
                self.service_prices = json.load(f)
        else:
            # default services
            self.service_prices = {
                "Adult HairCut": 25.00,
                "Adult HairCut & Dye": 40.00,
                "Kids HairCut": 15.00,
                "Kids HairCut & Bye": 30.00,
                "Hair Washing": 15.00,
                "Dye": 15.00,
                "colored Dye": 60.00,
            }
            with open(self.services_path, "w", encoding="utf-8") as f:
                json.dump(self.service_prices, f, indent=2)

                #Service dropdown
        self.service_type = ctk.CTkOptionMenu(
            sales_frame,
            values=list(self.service_prices.keys()),
            fg_color="#5DADE2",
            corner_radius=12,
            width=300, height=30,
            command=self.on_service_selected
        )
        self.service_type.set("Select Service")
        self.service_type.place(relx=0.4, rely=0.3, anchor="center")


        # Amount entry
        self.amount_entry = ctk.CTkEntry(sales_frame, placeholder_text="e.g., 25.00", corner_radius=12, width=200)
        self.amount_entry.place(relx=0.4, rely=0.38, anchor="center")
      
        # Status label
        self.status_label = ctk.CTkLabel(sales_frame, text="", text_color="white")
        self.status_label.place(relx=0.4, rely=0.455, anchor="center")

        # Record Sale button
        self.record_btn = ctk.CTkButton(
            sales_frame, text="RECORD SALE", command=self.on_record_sale,
            font=ctk.CTkFont(size=16, weight="bold"), corner_radius=20, width=150, height=50,
            fg_color="#1ABC9C", hover_color="#45a049", text_color="white"
        )
        self.record_btn.place(relx=0.4, rely=0.54, anchor="center")


    def on_service_selected(self, service_name):
        self.amount_entry.delete(0, "end")
        price = self.service_prices.get(service_name)
        if price is not None:
            self.amount_entry.insert(0, f"{price:.2f}")

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
    
# ──────────────────────────────────────────────────────────────sidebar_elements─────
    # ─── Admin panel opener ────

    def open_admin_panel(self):
        # 1) Prevent multiple panels
        # Toggle: if already open, close it
        if hasattr(self, "admin_window") and self.admin_window.winfo_exists():
            self.admin_window.destroy()
            return


        # 2) Create the panel window
        self.admin_window = ctk.CTkToplevel(self)
        win = self.admin_window
        win.title("Admin Panel")
        win.geometry("300x400+40+15")
        win.resizable(False, False) # Fixed size
        win.transient(self)
        win.attributes("-topmost", True)
        win.focus_force()

        # 3) Container for buttons
        panel = ctk.CTkFrame(win, fg_color="#222222")
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        # 4) Define actions and pack buttons
        actions = [
            ("Reset Data",     self.reset_data),
            ("Add Barber",     self.add_barber),
            ("Remove Barber",  self.remove_barber),   # ← NEW
            ("Add Service",    self.add_services),
            ("Remove Service", self.remove_service),
            ("Delete Sale", self.remove_sale),
            ("Reset Password", self.reset_password),
            ("Help",           self.show_help_window)
        ]
        for text, cmd in actions:
            btn = ctk.CTkButton(
                panel,
                text=text,
                fg_color="#1ABC9C",
                text_color="white",
                corner_radius=8,
                height=35,
                command=cmd
            )
            btn.pack(fill="x", pady=5)

    def add_barber(self):
        import os, json
        from tkinter import simpledialog, messagebox
        # 1) Ask for the new barber name
        name = self.prompt_dialog(
            "Add Barber",
            "Enter new barber name:",
            width=400,
            height=180,)

        if not name:
            return
        name = name.strip()
        if not name:
            return

        # 2) Read existing list
        try:
            with open(CONSTS.BARBER_TXT, "r", encoding="utf-8") as f:
                barbers = [b.strip() for b in f if b.strip()]
        except FileNotFoundError:
            barbers = []

        if name in barbers:
            messagebox.showwarning("Exists", f"Barber '{name}' already exists.", parent=self.admin_window)
            return

        # 3) Append, persist to barbers.txt and all_barbers.json
        barbers.append(name)
        with open(CONSTS.BARBER_TXT, "w", encoding="utf-8") as f:
            f.write("\n".join(barbers))
        with open(CONSTS.ALL_JSON, "w", encoding="utf-8") as f:
            json.dump(barbers, f, indent=2)

        # 4) Create individual file
        filename = CONSTS.BARBER_JSON_TMPL.format(name)
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as bf:
                json.dump([], bf)

        # 5) Update dropdown in the view
        self.update_barber_names(barbers)
        messagebox.showinfo("Added", f"Barber '{name}' added.", parent=self.admin_window)



    def add_services(self):
        from tkinter import messagebox

        # 3a) Ask for the service name
        name = self.prompt_dialog(
            "Add Service",
            "Enter new service name:",
            width=400, height=180
        )
        if not name or not name.strip():
            return
        name = name.strip()
        if name in self.service_prices:
            messagebox.showwarning("Exists", f"Service '{name}' already exists.", parent=self.admin_window)
            return

        # 3b) Ask for its standard price
        price_str = self.prompt_dialog(
            "Service Price",
            f"Enter standard price for '{name}':",
            width=300, height=150
        )
        try:
            price = float(price_str)
        except:
            messagebox.showerror("Error", "Invalid price entered.", parent=self.admin_window)
            return

        # 3c) Update in‑memory dict and write file
        self.service_prices[name] = price
        with open(self.services_path, "w", encoding="utf-8") as f:
            json.dump(self.service_prices, f, indent=2)

        # 3d) Update the dropdown in the UI
        self.service_type.configure(values=list(self.service_prices.keys()))
        messagebox.showinfo("Added", f"Service '{name}' added at price GHS{price:.2f}.",
                            parent=self.admin_window)
   
    def remove_barber(self):
        from tkinter import messagebox

        # 1) Ask which barber
        name = self.prompt_dialog(
            "Remove Barber",
            "Enter the exact name of the barber to remove:",
            width=400, height=180
        )
        if not name or not name.strip():
            return
        name = name.strip()

        # 2) Confirm they exist
        if name not in self.barber_names:
            messagebox.showerror(
                "Not Found",
                f"No barber named '{name}'",
                parent=self.admin_window
            )
            return

        # 3) Protect with admin password
        pwd = simpledialog.askstring(
            "Confirm Deletion",
            f"Enter admin password to remove '{name}':",
            show="*",
            parent=self.admin_window
        )
        if pwd != "@1234":   # must match your admin pass
            messagebox.showerror(
                "Denied",
                "Incorrect password—action cancelled.",
                parent=self.admin_window
            )
            return

        # 4) Remove from barbers.txt and all_barbers.json
        try:
            # update list
            new_list = [b for b in self.barber_names if b != name]
            # write barbers.txt
            with open(CONSTS.BARBER_TXT, "w", encoding="utf-8") as f:
                f.write("\n".join(new_list))
            # write all_barbers.json
            with open(CONSTS.ALL_JSON, "w", encoding="utf-8") as f:
                json.dump(new_list, f, indent=2)
            # delete the barber's own JSON file
            path = CONSTS.BARBER_JSON_TMPL.format(name)
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to remove barber data: {e}",
                parent=self.admin_window
            )
            return

        # 5) Update in‑memory and UI
        self.barber_names = new_list
        self.update_barber_names(new_list)
        messagebox.showinfo(
            "Removed",
            f"Barber '{name}' and all their data have been deleted.",
            parent=self.admin_window
        )


    def remove_service(self):
        from tkinter import messagebox

        # 1) Ask which service
        svc = self.prompt_dialog(
            "Remove Service",
            "Enter the exact service name to remove:",
            width=400, height=180
        )
        if not svc or not svc.strip():
            return
        svc = svc.strip()

        # 2) Confirm it exists
        if svc not in self.service_prices:
            messagebox.showerror(
                "Not Found",
                f"No service named '{svc}'",
                parent=self.admin_window
            )
            return

        # 3) Remove from dict and persist
        try:
            del self.service_prices[svc]
            with open(self.services_path, "w", encoding="utf-8") as f:
                json.dump(self.service_prices, f, indent=2)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to remove service: {e}",
                parent=self.admin_window
            )
            return

        # 4) Update the dropdown
        self.service_type.configure(values=list(self.service_prices.keys()))
        messagebox.showinfo(
            "Removed",
            f"Service '{svc}' has been removed.",
            parent=self.admin_window
        )

    def remove_sale(self):
        from tkinter import messagebox

        # 1) Ask which barber
        barber = self.prompt_dialog(
            "Remove Sale",
            "Enter the barber name whose sale you want to delete:",
            width=400, height=180
        )
        if not barber or barber.strip() not in self.barber_names:
            messagebox.showerror("Error", "Invalid or unknown barber.", parent=self.admin_window)
            return
        barber = barber.strip()

        # 2) Load that barber's sales file
        path = CONSTS.BARBER_JSON_TMPL.format(barber)
        if not os.path.exists(path):
            messagebox.showinfo("No Data", f"No sales found for {barber}.", parent=self.admin_window)
            return
        with open(path, "r", encoding="utf-8") as f:
            records = json.load(f)
        if not records:
            messagebox.showinfo("No Data", f"No sales found for {barber}.", parent=self.admin_window)
            return

        # 3) Build a preview list
        preview = []
        for idx, r in enumerate(records, 1):
            # convert timestamp to human‐friendly
            ts = r.get("time", r.get("date", ""))
            try:
                dt = datetime.fromisoformat(ts)
                ts = dt.strftime("%d/%m/%Y %H:%M")
            except:
                pass
            preview.append(f"{idx}. {ts} — {r.get('service','')} — ₵{float(r.get('amount',0)):.2f}")
        # show it in a scrollable dialog
        messagebox.showinfo(
            f"{barber}ʼs Sales",
            "\n".join(preview),
            parent=self.admin_window
        )

        # 4) Prompt for the index to delete
        idx_str = self.prompt_dialog(
            "Delete Sale",
            f"Enter the sale number to delete (1–{len(records)}):",
            width=350, height=150
        )
        try:
            idx = int(idx_str) - 1
            if idx < 0 or idx >= len(records):
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid sale number.", parent=self.admin_window)
            return

        # 5) Delete and save
        removed = records.pop(idx)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        messagebox.showinfo(
            "Removed",
            f"Removed sale #{idx+1}: {removed.get('service')} ₵{removed.get('amount'):.2f}",
            parent=self.admin_window
        )

        # 6) If the View Sales window is open, refresh it
        if hasattr(self, "sales_window") and self.sales_window.winfo_exists():
            self.view_sales()

    def reset_password(self):
        print("reset password clicked")
        # TODO: implement settings dialog

    def reset_data(self):
        from tkinter import messagebox

        # 1) Ask for admin password via custom dialog
        pwd = self.prompt_dialog(
            "Confirm Reset",
            "Enter admin password to clear ALL data:",
            width=350, height=150,
            show="*"
        )
        if pwd is None:
            return   # user cancelled
        if pwd != "@1234":   # match your real admin password
            messagebox.showerror(
                "Denied",
                "Incorrect password—reset cancelled.",
                parent=self.admin_window
            )
            return

        # 2) Confirm reset
        if not messagebox.askyesno(
            "Are You Sure?",
            "This will clear ALL sales and ALL expenses. Continue?",
            parent=self.admin_window
        ):
            return

        # 3) Clear each barber’s JSON
        for name in self.barber_names:
            path = CONSTS.BARBER_JSON_TMPL.format(name)
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump([], f)
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to clear {name}'s sales: {e}",
                    parent=self.admin_window
                )
                return

        # 4) Clear expense.json
        exp_path = os.path.join(os.path.dirname(__file__), "..", "expense.json")
        try:
            with open(exp_path, "w", encoding="utf-8") as f:
                json.dump([], f)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to clear expenses: {e}",
                parent=self.admin_window
            )
            return

        # 5) Feedback + refresh any open windows
        messagebox.showinfo(
            "Reset Complete",
            "All sales and expenses have been cleared.",
            parent=self.admin_window
        )
        if hasattr(self, "sales_window") and self.sales_window.winfo_exists():
            self.view_sales()
        if hasattr(self, "expense_window") and self.expense_window.winfo_exists():
            self.refresh_expense_view()


    #_____generate_summary___

    def generate_sales_summary(self):
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

        lines = []
        lines.append("SALES REPORT")
        lines.append("")
        def sort_key(date_str):
            try:
                return (0, datetime.strptime(date_str, "%A, %d/%m/%Y"))
            except Exception:
                return (1, date_str)

        for barber, recs in sorted(sales_by_barber.items()):
            lines.append(f"___________________________\n\n{barber}\n___________________________")
            lines.append("")
            lines.append("Sales:")
            lines.append("")

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
            for date_str in sorted(by_date.keys(), key=sort_key):
                items = by_date[date_str]
                lines.append(date_str)
                lines.append("")

                daily_total = 0.0
                for r in items:
                    svc = r.get("service", "<no service>")
                    amt = float(r.get("amount", 0))
                    daily_total += amt
                    lines.append(f"  • {svc}: GHS{amt:.2f}")

                lines.append("")
                lines.append(f"  Daily Sub-total: GHS{daily_total:.2f}")
                lines.append("")
                overall_total += daily_total

            lines.append(f"Total Sales: GHS{overall_total:.2f}")
            commission = overall_total / 3.0
            lines.append(f"Barber's Commission: GHS{commission:.2f}")
            lines.append("")
        expense_summary, total_expense = self.generate_expense_summary()
        lines.append("_________________________________________________________________________")
        lines.append("")
        lines.append("All Expenses:")
        lines.append("")
        lines.append(expense_summary)
        lines.append("")
        lines.append("_________________________________________________________________________\n" \
        "_________________________________________________________________________")
        lines.append("")
        all_barbers_overall_total = 0.0
        for barber, recs in sales_by_barber.items():
            for r in recs:
                amt = float(r.get("amount", 0))
                all_barbers_overall_total += amt
        lines.append(f" Overall Total Sales: GHS{all_barbers_overall_total:.2f}")
        lines.append("")
        overall_commission = all_barbers_overall_total / 3.0
        lines.append(f" Overall Commission : GHS{overall_commission:.2f}")
        lines.append("")
        lines.append(f" Total expenses : GHS{total_expense:.2f}")
        lines.append("")
        lines.append(f" Total Amount left : GHS{(all_barbers_overall_total -( total_expense + overall_commission)):.2f}")    

        return "\n".join(lines) if lines else "No sales data found."


    def view_sales(self):

        # — Prevent multiple windows and ensure front focus —
        if hasattr(self, "sales_window") and self.sales_window.winfo_exists():
            self.sales_window.lift()
            self.sales_window.focus_force()
            return

        summary = self.generate_sales_summary()
        if not summary:
            self.set_status("No sales data found.", success=False)
            return

        # 5) Show in a scrollable toplevel window
        self.sales_window = ctk.CTkToplevel(self)
        win = self.sales_window
        win.title("All Sales by Barber")
        win.geometry("500x600+15+20")
        win.resizable(False, False)

        # Keep it on top of the main application window
        win.transient(self.master)
        win.attributes("-topmost", True)
        win.focus_force()

        box = ctk.CTkTextbox(win, width=480, height=560, wrap="word")
        box.pack(padx=10, pady=10, fill="both", expand=True)
        box.insert("1.0", summary)
        box.configure(state="disabled")

    def show_help_window(self):
        # prevent multiple
        if hasattr(self, "help_window") and self.help_window.winfo_exists():
            self.help_window.lift()
            return

        # parent must be a widget, not the controller
        self.help_window = ctk.CTkToplevel()
        win = self.help_window
        win.title("Help")
        win.geometry("630x500+200+40")
        win.transient(admin_window := self.admin_window if hasattr(self, "admin_window") else self.master)
        win.attributes("-topmost", True)
        win.focus_force()

        text_widget = ctk.CTkTextbox(
            win,
            width=430,
            height=300,
            wrap="word",
            font=("Arial", 14),
            text_color="white",
            fg_color="#333333"
        )
        text_widget.pack(pady=10, padx=10, fill="both", expand=True)

        text_widget.insert("1.0", CONSTS.HELP_TEXT or "No help content available.")
        text_widget.configure(state="disabled")


    def export(self):
        # Re-generate the sales summary string
        if not hasattr(self, "view_sales"):
            return  # Safety check
        #generate the the sales summary lines
        summary_lines = self.generate_sales_summary()  # Implement this based on view_sales
        if not summary_lines:
            return

        # Ask where to save the PDF
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Sales Summary as PDF"
        )

        if not file_path:
            return  # User cancelled

        # Create PDF
        c = canvas.Canvas(file_path, pagesize=LETTER)
        width, height = LETTER
        margin = 40
        y = height - margin

        for line in summary_lines.split("\n"):
            if y < margin:
                c.showPage()
                y = height - margin
            c.drawString(margin, y, line)
            y -= 14  # Line spacing

        c.save()
        messagebox.showinfo("Export Successful", f"Sales summary exported to {file_path}")
        self.set_status("Sales summary exported successfully.", success=True)
    

    def generate_expense_summary(self):
        """Load expense.json and return a summary string with per‑item totals and grand total."""
        import os, json
        from datetime import datetime

        path = os.path.join(os.path.dirname(__file__), "..", "expense.json")
        if not os.path.exists(path):
            data = []
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

        lines = []
        total_expense = 0.0

        for idx, rec in enumerate(data, 1):
            # Safely parse quantity
            raw_qty = rec.get("quantity", 1)
            try:
                qty = int(raw_qty)
            except (ValueError, TypeError):
                qty = 1

            # Safely parse amount
            raw_amt = rec.get("amount", 0)
            try:
                amt = float(raw_amt)
            except (ValueError, TypeError):
                amt = 0.0

            item = rec.get("item", "<no item>")

            # Compute cost for this line
            cost = qty * amt
            total_expense += cost

            # Parse date (day name, DD/MM/YYYY)
            date = rec.get("date", "")
            try:
                dt = datetime.fromisoformat(date)
                date = dt.strftime("%A, %d/%m/%Y")
            except Exception:
                pass

            # Build the line: show unit price and line‑total
            lines.append(
                f"{idx}. {item} x{qty} @ GHS{amt:.2f} each = GHS{cost:.2f}  ({date})\n"
            )

        # Add a blank line before the grand total
        total_expense = round(total_expense, 2)  # Round to 2 decimal places
        lines.append("")
        lines.append(f"Total Expense: GHS{total_expense:.2f}")

        summary= "\n".join(lines) if lines else "No expenses recorded."
        return (summary, total_expense)


    def on_view_expense(self):
        # — Prevent multiple windows —
        if hasattr(self, "expense_window") and self.expense_window.winfo_exists():
            self.expense_window.destroy()
            return

        self.expense_window = ctk.CTkToplevel(self)
        win = self.expense_window
        win.title("View Expenses")
        win.geometry("700x600+820+30")
        win.resizable(False, False)
        win.transient(self.master)
        win.attributes("-topmost", True)

        # Sidebar
        shadow = ctk.CTkFrame(win, width=700, fg_color="#008080", corner_radius=0)
        shadow.place(x=0, y=0, relheight=1)
        self.sidebar = ctk.CTkFrame(win, fg_color="#1A1F2B", corner_radius=0)
        self.sidebar.place(x=5, y=5, relheight=0.98)  # instead of relheight=1


        # Logo
        logo = ctk.CTkLabel(self.sidebar, text="🧔 Expenses")
        logo.pack(pady=20)

        # (Optional) keep a thin separator under the logo
        sep_top = ttk.Separator(self.sidebar, orient="horizontal")
        sep_top.pack(fill="x", pady=(0,10), padx=20)

        # 1) Item entry
        ctk.CTkLabel(self.sidebar, text="Item:").pack(pady=(10,2))
        self.expense_item_entry = ctk.CTkEntry(
            self.sidebar, placeholder_text="e.g., shampoo", width=160
        )
        self.expense_item_entry.pack(pady=(0,10))

        # 2) Amount entry
        ctk.CTkLabel(self.sidebar, text="Amount:").pack(pady=(0,2))
        self.expense_amount_entry = ctk.CTkEntry(
            self.sidebar, placeholder_text="e.g., 25.00", width=160
        )
        self.expense_amount_entry.pack(pady=(0,10))

        # 3) Quantity dropdown
        ctk.CTkLabel(self.sidebar, text="Quantity:").pack(pady=(0,2))
        self.quantity_dropdown = ctk.CTkOptionMenu(
            self.sidebar, values=[str(i) for i in range(1,11)],
            fg_color="#1ABC9C", width=160
        )
        self.quantity_dropdown.set("Select")
        self.quantity_dropdown.pack(pady=(0,20))

        # 4) Add Expense button
        add_btn = ctk.CTkButton(
            self.sidebar, text="Add Expense", fg_color="#E0E0E0",
            text_color="#1A1F2B", corner_radius=8,
            width=160, height=30, command=self.add_expense
        )
        add_btn.pack(padx=20, pady=(0,10))

        # 5) Separator between buttons
        sep_mid = ttk.Separator(self.sidebar, orient="horizontal")
        sep_mid.pack(fill="x", pady=10, padx=20)

        # 6) Delete Expense button
        del_btn = ctk.CTkButton(
            self.sidebar, text="Delete Expense", fg_color="#E74C3C",
            text_color="#1A1F2B", corner_radius=8,
            width=160, height=30, command=self.delete_expense
        )
        del_btn.pack(padx=20, pady=(0,10))


        # Textbox
        self.expense_textbox = ctk.CTkTextbox(win, width=482, height=590, wrap="word")
        self.expense_textbox.place(x=212, y=6, anchor="nw")
        self.expense_textbox.configure(state="disabled")

        # Initial load
        self.refresh_expense_view()


    def refresh_expense_view(self):
        """Load expense.json with generate_expense_summary() method and display  its contents in the textbox."""
        expense_summary, total_expense = self.generate_expense_summary()
        self.expense_textbox.configure(state="normal")
        self.expense_textbox.delete("1.0", "end")
        self.expense_textbox.insert("1.0",expense_summary)
        self.expense_textbox.configure(state="disabled")


    def add_expense(self):
        item = self.expense_item_entry.get().strip()
        amount = self.expense_amount_entry.get().strip()
        qty = self.quantity_dropdown.get()
        if not item or not amount or qty == "Select":
            messagebox.showerror("Error", "Please fill item, amount, and quantity.", parent=self.expense_window)
            return
        try:
            amt_val = float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number.",parent=self.expense_window)
            return

        rec = {
            "item": item,
            "amount": amt_val,
            "quantity": int(qty),
            "date": datetime.now().isoformat()
        }

        path = os.path.join(os.path.dirname(__file__), "..", "expense.json")
        data = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        data.append(rec)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.expense_item_entry.delete(0, "end")
        self.expense_amount_entry.delete(0, "end")
        self.quantity_dropdown.set("Select")
        self.refresh_expense_view()


    def delete_expense(self):
        # Ask user for the index to delete
        # idx_str = simpledialog.askstring("Delete Expense", "Enter expense number to delete:", parent=self.expense_window)
        idx_str  = self.prompt_dialog(
            "Delete Expense", "Enter expense number to delete:",

            width=400,
            height=180)



        if not idx_str:
            return
        try:
            idx = int(idx_str) - 1
        except:
            messagebox.showerror("Error", "Invalid number.",parent=self.expense_window)
            return

        path = os.path.join(os.path.dirname(__file__), "..", "expense.json")
        if not os.path.exists(path):
            messagebox.showinfo("Info", "No expense file found.",parent=self.expense_window)
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if idx < 0 or idx >= len(data):
            messagebox.showerror("Error", "Number out of range.",parent=self.expense_window)
            return

        data.pop(idx)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.refresh_expense_view()



    def prompt_dialog(self, title, prompt, width=400, height=200, show=None):
        """
        Displays a modal CTkToplevel aligned to the right side of the screen,
        with a label and entry. Returns the entered string, or None if cancelled.
        """
        # 1) Determine parent window and screen dimensions
        parent = self.master.winfo_toplevel()  # the CTk root
        screen_w = parent.winfo_screenwidth()
        screen_h = parent.winfo_screenheight()

        # 2) Compute X so dialog's right edge is 20px from screen right
        x = screen_w - width - 20
        # 3) Compute Y so dialog is vertically centered (or offset as you like)
        y = (screen_h - height) // 2

        # 4) Create the dialog
        dlg = ctk.CTkToplevel(parent)
        dlg.title(title)
        dlg.geometry(f"{width}x{height}+{x}+{y}")
        dlg.transient(parent)
        dlg.grab_set()   # modal
        dlg.attributes("-topmost", True)
        dlg.focus_force()

        # Prompt text
        lbl = ctk.CTkLabel(dlg, text=prompt, wraplength=width-40)
        lbl.pack(pady=(20,10), padx=20)

        entry = ctk.CTkEntry(dlg, width=width-40, show=show)
        entry.pack(pady=(0,20), padx=20)
        entry.focus()

        result = {"value": None}

        def on_ok():
            result["value"] = entry.get()
            dlg.destroy()

        def on_cancel():
            dlg.destroy()

        btn_frame = ctk.CTkFrame(dlg, fg_color="transparent")
        btn_frame.pack(pady=(0,20))
        ok = ctk.CTkButton(btn_frame, text="OK", width=80, command=on_ok)
        ok.pack(side="left", padx=10)
        cancel = ctk.CTkButton(btn_frame, text="Cancel", width=80, command=on_cancel)
        cancel.pack(side="left", padx=10)

        dlg.wait_window()
        return result["value"]




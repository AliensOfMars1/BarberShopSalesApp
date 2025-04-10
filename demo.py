import customtkinter as ctk
from datetime import datetime

# Initialize customtkinter
ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("blue")

# Dummy barbers list
barbers = ["Mike", "Alex", "Sasha", "Jordan"]

# Sale records list
sales_log = []

# Record function
def record_sale():
    barber = barber_dropdown.get()
    customer = customer_entry.get()
    amount = amount_entry.get()

    if not customer or not amount:
        status_label.configure(text="Please fill all fields.", text_color="red")
        return

    try:
        sale = float(amount)
    except ValueError:
        status_label.configure(text="Amount must be a number.", text_color="red")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sale_record = {
        "barber": barber,
        "customer": customer,
        "amount": sale,
        "time": timestamp
    }

    sales_log.append(sale_record)

    status_label.configure(text=f"Sale recorded for {customer}.", text_color="green")
    customer_entry.delete(0, ctk.END)
    amount_entry.delete(0, ctk.END)

# GUI setup
app = ctk.CTk()
app.title("Barbershop Sales Recorder")
app.geometry("400x350")

title_label = ctk.CTkLabel(app, text="Barbershop Sales", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

barber_dropdown = ctk.CTkOptionMenu(app, values=barbers)
barber_dropdown.set(barbers[0])
barber_dropdown.pack(pady=10)

customer_entry = ctk.CTkEntry(app, placeholder_text="Customer Name")
customer_entry.pack(pady=10)

amount_entry = ctk.CTkEntry(app, placeholder_text="Sale Amount")
amount_entry.pack(pady=10)

record_button = ctk.CTkButton(app, text="Record Sale", command=record_sale)
record_button.pack(pady=20)

status_label = ctk.CTkLabel(app, text="", font=("Arial", 12))
status_label.pack(pady=10)

app.mainloop()

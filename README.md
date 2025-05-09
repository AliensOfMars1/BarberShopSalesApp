PROJECT STRUCTURE 
.
├── a_consts.py            # Paths for barbers.txt, all_barbers.json, credentials.json, expense.json, etc.
├── credentials.json       # Persisted admin credentials (auto-generated)
├── expense.json           # Expense records
├── services.json          # Services → prices map
├── barbers.txt            # Comma-separated barber list
├── all_barbers.json       # JSON-array of barber names
├── main.py                # Application entry point
├── models/
│   └── model.py           # SalesModel: in-memory sales log & credentials
├── controllers/
│   ├── setup_controller.py
│   └── sales_controller.py
└── views/
    ├── setup_view.py
    └── sales_view.py



# BarberApp

A lightweight desktop application to manage barber shop sales, services, expenses, and reporting—built with Python, CustomTkinter, and ReportLab.

---

## Features

- *Initial Setup* 
  - Enter comma-separated barber names on first launch.  
  - Saves to barbers.txt, all_barbers.json, and per-barber JSON files.

- *Sales Recording*
  - Select a barber and service, auto-populate prices, edit amount as needed.  
  - Record sale with timestamp; in-memory log plus per-barber JSON persistence.

- *Sales History & Reporting*
  - View session history in a dialog.  
  - “View Sales” window: grouped by barber and date, daily subtotals, commissions.  
  - Export full report to PDF via ReportLab.

- *Expense Tracking*
  - Add/delete expense items with quantity and date.  
  - View an itemized summary with grand total.  
  - Included in overall sales report.

- *Admin Panel* 
  - *Reset Data*: Clear all sales and expenses (admin password protected).  
  - *Add/Remove Barber*: Manage your team; updates files and dropdown.  
  - *Add/Remove Service*: Customize services and standard prices.  
  - *Delete Sale*: Remove specific sale records.  
  - *Reset Password*: Change the admin password (persisted across restarts).  
  - *Help*: Built-in help text for every admin action.

- *Full “Reset App”*  
  - Clears barbers, sales, expenses, credentials file → back to first-run state.


TO RUN THIS APP
1. clone this repo
2. create a virtual environment
3. intall the requirements.txt
4. Run scripts from the app entry : python main.py 



# Constants for the Barber Sales Recorder application
import os 
class CONSTS:
    # Constants for the application
    APP_NAME = "Sporky Barbers - Sales Recoder"
    VERSION = "version 1.0.0"
    AUTHOR = "Prince Anane"
    BARBER_TXT   = "barbers.txt"
    BARBER_TXT     = "barbers.txt"
    ALL_JSON       = "all_barbers.json"
    BARBER_JSON_TMPL = "{}.json"
    BARBER_JSON     = "barbers.json"
    EXPENSES_JSON = "expenses.json"
    CREDENTIALS_JSON = os.path.join(os.path.dirname(__file__), "credentials.json")

    HELP_TEXT = """
        Welcome to Sales-Recorder Help! Here's how to use all the features:

        • First-Time Setup:

            On your first launch, enter your barber names (comma-separated) and click “Proceed.”
            This creates your roster and initializes the app.

            
        • Recording a Sale:
            1. Select a barber from the dropdown.
            2. Select a service (price will auto-fill).
            3. Adjust the amount if needed.
            4. Click “Record Sale.”

            
        • Viewing History:
            Click the History-button in the sidebar to see all sales recorded in this session.

            
        • Viewing All Sales:
            Click View Sales in the sidebar to open a detailed report:
                - Grouped by barber and date
                - Daily subtotals and total sales
                - Barber commission totals
                - Expense summary and overall totals

                
        • Exporting to PDF:

            Click Export in the sidebar, choose a filename, and save your full sales & expense 
            report as a PDF.

            
        • Managing Expenses:

            1. Click “View Expense” in the sidebar.
            2. In the expense panel, enter an item, amount, and quantity.
            3. Click “Add Expense” to record it.
            4. To delete, click “Delete Expense” and enter the item number.
            The summary on the right updates automatically.

            
        • Admin Panel (click “Admin” in the sidebar):

            - Reset Data: Clears all sales & expenses but keeps your barber roster.

               • When to use: At the start of a new accounting period,
                 or if you need to purge all data and start fresh.
            
            - Add / Remove Barber: Manage your team; updates dropdown and files.
            - Add / Remove Service: Customize services and prices.
            - Delete Sale: Remove a single sale record by barber and record number.
            - Reset Password: Change the admin password (protected by the current password).
            - Help: Reopen this help dialog.

        • Full Reset (sidebar “Reset App”):
            Completely wipes barbers, sales, expenses, and resets admin password to default.
            Use with caution to start fresh.

        • Security:
            All admin actions require the admin password. Keep it safe and change it regularly.

        For further assistance, contact Developer at princemolly405@gmail.com.
    """

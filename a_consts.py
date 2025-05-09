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
        Welcome to BarberApp Help!

        • To Record Sales: Select a barber, choose a service, enter the amount,
        then click “Record Sale.” 

        • To View History: Click “History.”  

        • To Reset the App: Click “Reset” and enter admin credentials.

        • To Export PDF: Click “Export” and choose a filename. 

        • To View Sales: Click “View Sales.” 

        • To Manage Expenses: Click “View Expense.”
        

        For more assistance, contact Developer at princemolly405@gmail.com.
        """

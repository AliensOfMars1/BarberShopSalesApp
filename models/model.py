from datetime import datetime
from a_consts import CONSTS
import os 
import json

class SalesModel:
    def __init__(self):
        self.barbers = []
        self.sales_log = []
        self.creds_path = CONSTS.CREDENTIALS_JSON
        if os.path.exists(self.creds_path):
            with open(self.creds_path, "r", encoding = "utf-8") as file:
                self.admin_credentials = json.load(file)
        else:
            self.admin_credentials = {"admin": "@1234"}
            self._save_credentials()

    def _save_credentials(self):
        with open(self.creds_path, "w", encoding = "utf-8") as file:
            json.dump(self.admin_credentials, file, indent=2)      

    def verify_admin(self, username, password):
        return self.admin_credentials.get(username) == password

    def change_password(self, username, current_pw, new_pw):
        # only allow if current matches
        if self.verify_admin(username, current_pw):
            self.admin_credentials[username] = new_pw
            self._save_credentials() 
            return True
        else:
            return False

    def record_sale(self, barber, service, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sale = {
            "barber": barber,
            "service": service,
            "amount": float(amount),
            "time": timestamp
        }
        self.sales_log.append(sale)
        return sale

    def get_sales_log(self):
        return self.sales_log

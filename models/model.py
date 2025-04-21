from datetime import datetime

class SalesModel:
    def __init__(self):
        self.barbers = ["Mike", "Alex", "Sasha", "Jordan"]
        self.sales_log = []
        self.admin_credentials = {"sporky": "1234"}

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

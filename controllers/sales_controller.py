# ============ controllers/sales_controller.py ============
from views.sales_view import SalesView

class SalesController:
    def __init__(self, root, barber_names):
        # Display sales frame
        self.frame = SalesView(root, barber_names)
        self.frame.pack(fill="both", expand=True)
    
    def update_barber_names(self, barber_names):
        # Update the barber names in the view
        self.frame.barber_dropdown.configure(values=barber_names)

        
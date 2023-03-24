from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def payment_entry():
    payment_entry_custom_fields()
    property_setter()
    
def payment_entry_custom_fields():
    pass
    
def property_setter():
    make_property_setter("Payment Entry", "paid_from", "reqd", 0, "Check")
    make_property_setter("Payment Entry", "paid_from", "hidden", 1, "Check")
    make_property_setter("Payment Entry", "paid_from_account_currency", "reqd", 0, "Check")
    make_property_setter("Payment Entry", "paid_from_account_currency", "hidden", 1, "Check")
    make_property_setter("Payment Entry", "paid_to_account_currency", "reqd", 0, "Check")
    make_property_setter("Payment Entry", "paid_to_account_currency", "hidden", 1, "Check")
    

def execute():
    payment_entry()

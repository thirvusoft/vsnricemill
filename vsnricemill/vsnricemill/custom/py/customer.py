import frappe
import re

def validate_phone_number(doc, actions):
    phone_pattern = r'^(\+91[-\s]?)?[0]?(91)?[789]\d{9}$'
    if re.match(phone_pattern, doc.mobile_no):
        frappe.msgprint("Phone number is valid.")
        return True
    else:
        frappe.throw("Phone number is not valid.")
        return False


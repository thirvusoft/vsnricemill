import frappe
import re

def validate_phone_number(doc, actions):
    if doc.mobile_no:
        phone_pattern = r'^(\+91[-\s]?)?[0]?(91)?[789]\d{9}$'
        if re.match(phone_pattern, doc.mobile_no):
            return
        else:
            frappe.throw("Phone number is not valid.")


import frappe
from frappe.model.naming import make_autoname


def auto_name(doc, actions):
    if(doc.is_pos==1):
        doc.name = make_autoname(doc.pos_series,doc=doc)
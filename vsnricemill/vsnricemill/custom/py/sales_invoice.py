import json
import frappe
from frappe.model.naming import make_autoname

def auto_name(doc, actions):
    if(doc.is_pos==1):
        doc.name = make_autoname(doc.pos_series,doc=doc)

def is_opening_name(doc, actions):
    if(doc.is_opening=="Yes"):
        doc.name = make_autoname(doc.opening_series,doc=doc)

@frappe.whitelist()
def get_attribute(items):
    item = json.loads(items)
    # for i in item:
    get_abb = frappe.db.get_value("Item Variant Attribute",{"parent":item.get('item_code'),"attribute":"Size"},"attribute_value")
    return get_abb

def validate(doc,event):
    for i in doc.items:
        i.size = frappe.db.get_value("Item Variant Attribute",{"parent":i.item_code,"attribute":"Size"},"attribute_value")

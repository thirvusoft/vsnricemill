import json
import frappe
from frappe.model.naming import make_autoname


def auto_name(doc, actions):
    if(doc.is_pos==1):
        doc.name = make_autoname(doc.pos_series,doc=doc)

@frappe.whitelist()
def get_attribute(items):
    item = json.loads(items)
    for i in item:
        get_abb = frappe.db.get_value("Item Variant Attribute",{"parent":i.get('item_code'),"attribute":"Size"},"attribute_value")
    print(get_abb,"----------")
    frappe.errprint(get_abb)
    return get_abb
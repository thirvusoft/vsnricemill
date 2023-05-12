import frappe

def print_name(doc,actions):
    if doc.brand:
        doc.print_name = doc.brand
        for i in doc.attributes:
            if not frappe.get_value("Item Attribute",i.attribute,"dont_set_in_item_print_name"):
                doc.print_name+=" "+frappe.get_value("Item Attribute Value",{"parent":i.attribute,"attribute_value":i.attribute_value},"abbr")
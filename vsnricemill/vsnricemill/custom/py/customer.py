import frappe

def captilized_name(doc,actions):
    doc.customer_name = doc.customer_name.capitalize()
    doc.name = doc.name.capitalize()


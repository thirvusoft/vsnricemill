import json
from erpnext.accounts.doctype.loyalty_program.loyalty_program import get_loyalty_program_details_with_points
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice, update_linked_doc
from erpnext.setup.doctype.company.company import update_company_current_month_sales
from erpnext.stock.doctype.serial_no.serial_no import update_serial_nos_after_submit
import frappe
from frappe.model.naming import make_autoname
from frappe.utils import add_days, cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate
from frappe import _, msgprint, throw


def auto_name(doc, actions):
    if(doc.pos_profile == "CounterSales VSN"):
        doc.name = make_autoname(f"{doc.name_series}.-.{doc.pos_series}.-.#####",doc=doc)
def counter_sales(doc, actions):
    if (doc.pos_profile == "JM Shop"):
      doc.name = make_autoname(f"{doc.c_sales}.-.{doc.pos_series}.-.#####",doc=doc)
    elif (doc.pos_profile == "CounterSales JM"):
       doc.name = make_autoname(f"{doc.name_series}.-.{doc.pos_series}.-.#####",doc=doc)
    elif (doc.branch == "JM Shop"):      
      doc.name = make_autoname(f"{doc.c_sales}.-.C.-.#####",doc=doc)

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

import frappe
from erpnext.accounts.party import get_dashboard_info
@frappe.whitelist()
def loyalty(customer,company):
 if customer:
  doc = frappe.get_doc("Customer",customer)
  data_points = get_dashboard_info(doc.doctype, doc.name, doc.loyalty_program)
  loyalty_points = 0
  for data_point in data_points:
   if 'loyalty_points' not in data_point:
    data_point['loyalty_points'] = 0
   if 'loyalty_points' in data_point:
    if company == data_point["company"]:
     loyalty_points = data_point['loyalty_points']
  return loyalty_points

import frappe
from erpnext.accounts.party import get_dashboard_info
def loyalty_validate(doc,event):
 if doc.customer:
  doc_ = frappe.get_doc("Customer",doc.customer)
  data_points = get_dashboard_info(doc_.doctype, doc_.name, doc_.loyalty_program)
  loyalty_points = 0
  for data_point in data_points:
   if 'loyalty_points' not in data_point:
    data_point['loyalty_points'] = 0
   if 'loyalty_points' in data_point:
    if doc.company == data_point["company"]:
     loyalty_points = data_point['loyalty_points']
     doc.existing_loyalty_point = loyalty_points

# def denomination_on_load(doc, actions):
#     if doc.posa_pos_opening_shift:
#         try:
#             opening_shift = frappe.get_doc("POS Opening Shift", doc.posa_pos_opening_shift)
#         except Exception as e:
#             frappe.log_error(f"Error fetching POS Opening Shift: {e}")
#             return
        
#         # create a dictionary of denomination counts
#         paid = {}
#         chang = {}
#         # for m in opening_shift.denomination_table:
#         #     counts[m.currency] = m.count
            
#         # update the counts based on paid denominations
#         for i in doc.paid_denomination:
#             if i.currency in paid:
#                 paid[i.currency] += i.count
#             else:
#                 paid[i.currency] = i.count
#         for c in doc.change_denomination:
#             if c:
#                 if c.currency in chang:
#                     chang[c.currency ] += c.count
#                 else:
#                     chang[c.currency] = c.count
        
#         # update the denomination_table list based on the updated counts
#         for m in opening_shift.denomination_table:
#             if m.currency in paid:
#                 m.count += (paid[m.currency] - chang[m.currency])
#                 m.amount = m.currency * m.count
                
#         opening_shift.save()
#     else:
#         return

# def cancel_denomination(doc,actions):
#     if doc.posa_pos_opening_shift:
#         cancel_opening_shift = frappe.get_doc("POS Opening Shift", doc.posa_pos_opening_shift)
#         for i in doc.paid_denomination:
#             for m in cancel_opening_shift.denomination_table:
#                 if i.currency == m.currency:
#                     m.count = m.count - i.count
#                     m.amount = m.amount - i.amount
        

# def print_name(doc,actions):
#    for i in doc.items:
#       variant = frappe.db.get_value("Item Variant Attribute",{"parent":i.item_code,"attribute":"Rice"},"attribute_value")
#       if variant:
#         r_vaiant = i.item_code.replace(variant, "")
#         new_print_name = r_vaiant.replace("  "," ")
#         i.print_name = new_print_name

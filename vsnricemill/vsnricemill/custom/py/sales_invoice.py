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
    if(doc.is_pos==1):
        doc.name = make_autoname(f"{doc.name_series}.-.{doc.pos_series}.-.#####",doc=doc)

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


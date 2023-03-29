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
 

# class vsnsalesInvoice(SalesInvoice):
    # def on_submit(self):
    #     self.validate_pos_paid_amount()

    #     if not self.auto_repeat:
    #         frappe.get_doc("Authorization Control").validate_approving_authority(
    #             self.doctype, self.company, self.base_grand_total, self
    #         )

    #     self.check_prev_docstatus()

    #     if self.is_return and not self.update_billed_amount_in_sales_order:
    #         # NOTE status updating bypassed for is_return
    #         self.status_updater = []

    #     self.update_status_updater_args()
    #     self.update_prevdoc_status()
    #     self.update_billing_status_in_dn()
    #     self.clear_unallocated_mode_of_payments()

    #     # Updating stock ledger should always be called after updating prevdoc status,
    #     # because updating reserved qty in bin depends upon updated delivered qty in SO
    #     if self.update_stock == 1:
    #         self.update_stock_ledger()
    #     if self.is_return and self.update_stock:
    #         update_serial_nos_after_submit(self, "items")

    #     # this sequence because outstanding may get -ve
    #     self.make_gl_entries()

    #     if self.update_stock == 1:
    #         self.repost_future_sle_and_gle()

    #     if not self.is_return:
    #         self.update_billing_status_for_zero_amount_refdoc("Delivery Note")
    #         self.update_billing_status_for_zero_amount_refdoc("Sales Order")
    #         self.check_credit_limit()

    #     self.update_serial_no()

    #     if not cint(self.is_pos) == 1 and not self.is_return:
    #         self.update_against_document_in_jv()

    #     self.update_time_sheet(self.name)

    #     if (
    #         frappe.db.get_single_value("Selling Settings", "sales_update_frequency") == "Each Transaction"
    #     ):
    #         update_company_current_month_sales(self.company)
    #         self.update_project()
    #     update_linked_doc(self.doctype, self.name, self.inter_company_invoice_reference)

    #     # create the loyalty point ledger entry if the customer is enrolled in any loyalty program
    #     if not self.is_return and not self.is_consolidated and self.loyalty_program:
    #         if self.status == "Paid":
    #             self.make_loyalty_point_entry()
    #     elif (
    #         self.is_return and self.return_against and not self.is_consolidated and self.loyalty_program
    #     ):
    #         against_si_doc = frappe.get_doc("Sales Invoice", self.return_against)
    #         against_si_doc.delete_loyalty_point_entry()
    #         against_si_doc.make_loyalty_point_entry()
    #     if self.redeem_loyalty_points and not self.is_consolidated and self.loyalty_points:
    #         self.apply_loyalty_points()

    #     self.process_common_party_accounting()
    # def make_loyalty_point_entry(self):
    #     returned_amount = self.get_returned_amount()
    #     current_amount = flt(self.net_total) - cint(self.loyalty_amount) #Core Code
    #     eligible_amount = current_amount - returned_amount
    #     lp_details = get_loyalty_program_details_with_points(
	# 		self.customer,
	# 		company=self.company,
	# 		current_transaction_amount=current_amount,
	# 		loyalty_program=self.loyalty_program,
	# 		expiry_date=self.posting_date,
	# 		include_expired_entry=True,
	# 	)
    #     if (
	# 		lp_details
	# 		and getdate(lp_details.from_date) <= getdate(self.posting_date)
	# 		and (not lp_details.to_date or getdate(lp_details.to_date) >= getdate(self.posting_date))
	# 	):
    #         collection_factor = lp_details.collection_factor if lp_details.collection_factor else 1.0
    #         points_earned = cint(eligible_amount / collection_factor)
    #         doc = frappe.get_doc(
	# 			{
	# 				"doctype": "Loyalty Point Entry",
	# 				"company": self.company,
	# 				"loyalty_program": lp_details.loyalty_program,
	# 				"loyalty_program_tier": lp_details.tier_name,
	# 				"customer": self.customer,
	# 				"invoice_type": self.doctype,
	# 				"invoice": self.name,
	# 				"loyalty_points": points_earned,
	# 				"purchase_amount": eligible_amount,
	# 				"expiry_date": add_days(self.posting_date, lp_details.expiry_duration),
	# 				"posting_date": self.posting_date,
	# 			}
	# 		)
    #         doc.flags.ignore_permissions = 1
    #         doc.save()
    #         self.set_loyalty_program_tier()
    # def get_returned_amount(self):
    #     from frappe.query_builder.functions import Coalesce, Sum
    #     doc = frappe.qb.DocType(self.doctype)
    #     returned_amount = (
    #         frappe.qb.from_(doc)
	# 		.select(Sum(doc.net_total)) #Core Code
	# 		.where(
	# 			(doc.docstatus == 1) & (doc.is_return == 1) & (Coalesce(doc.return_against, "") == self.name)
	# 		)
	# 	).run()
    #     return abs(returned_amount[0][0]) if returned_amount[0][0] else 0

	# # redeem the loyalty points.
    # def validate_pos_paid_amount(self):
    #     if len(self.payments) == 0 and self.is_pos:
    #        frappe.throw(_("At least one mode of payment is required for POS invoice."))


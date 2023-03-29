# # from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
# import frappe

# # class VsnPaymentEntry(PaymentEntry):
# def update_outstanding_amounts(self, event):
# 		for d in self.get("references"):
# 			if d.reference_doctype == "Sales Invoice" and d.outstanding_amount == 0:
# 				doc = frappe.get_doc(d.reference_doctype, d.reference_name)
# 				doc.make_loyalty_point_entry()
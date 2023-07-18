from erpnext.accounts.party import get_party_account
import frappe
from erpnext.accounts.utils import get_account_currency, get_balance_on, get_outstanding_invoices
from frappe.email.doctype.notification.notification import get_context
from frappe.integrations.doctype.slack_webhook_url.slack_webhook_url import send_slack_message
from erpnext.selling.doctype.customer.customer import get_customer_outstanding

def update(doc,actions):
    if doc.payment_type == "Pay":
        bank_account =  frappe.get_doc("Account",doc.paid_from)
        if bank_account.cc_account == 1:
            get_balance = bank_account.limit - bank_account.limit * 90 /100 
            bal = get_balance_on(doc.paid_from, date = None, cost_center=None)
            if bal < doc.paid_amount:
                send_slack_message(
                    webhook_url="Notify",
                    message=f'Your available balance is {bal} but you have initiated payment for {doc.paid_amount}',#frappe.render_template(doc.name, get_context(doc)),
                    reference_doctype=doc.doctype,
                    reference_name=doc.name,
                )
                frappe.msgprint(f'Your available balance is {bal} but you have initiated payment for {doc.paid_amount}')
            elif bal  < get_balance:
                send_slack_message(
                    webhook_url="Notify",
                    message=f"You have almost exhasuted your CC {doc.paid_from} limit",#frappe.render_template(doc.name, get_context(doc)),
                    reference_doctype=doc.doctype,
                    reference_name=doc.name,
                )
                frappe.msgprint(f"You have almost exhasuted your CC {doc.paid_from} limit")


def current_outstanding_amount(doc, actions=None):
        customer = doc.party  
        doc.current_outstanding_amount = get_customer_outstanding(customer,doc.company) 
        if actions == "before_submit":
            doc.current_outstanding_amount -= doc.paid_amount


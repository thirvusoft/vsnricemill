from erpnext.accounts.party import get_party_account
import frappe
from erpnext.accounts.utils import get_account_currency, get_balance_on, get_outstanding_invoices
from frappe.email.doctype.notification.notification import get_context
from frappe.integrations.doctype.slack_webhook_url.slack_webhook_url import send_slack_message
def update(doc,actions):
    if doc.payment_type == "Pay":
        bank_account =  frappe.get_list("Account",{'name':doc.paid_from},"limit")
        print(bank_account[0].limit - bank_account[0].limit * 90 /100  )
        get_balance = bank_account[0].limit - bank_account[0].limit * 90 /100 
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

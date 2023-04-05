import frappe
from vsnricemill.vsnricemill.custom.py.payment_entry import update
def slack_notify(doc,actions):
    doc=frappe.new_doc("Notification")
    doc.update({
        'doctype':'Notification',
        '__newname':"Slack Notify",
        'channel':'Slack',
        'subject':{doc.name},
        'conditon': update(doc,actions),
        'document_type':'Payment Entry',
        'event':'Save',
        'message': {doc.name},
        'send_to_all_assignees':True,
        'send_system_notification':True
    })
    doc.insert(ignore_permissions=True)
    doc.save()
import frappe

def make_contact_creation(doc,actions):
    if not frappe.db.exists("Contact", {'first_name':doc.address_title}):
        document=frappe.new_doc("Contact")
        document.first_name =doc.address_title
        document.append('email_ids', dict(
            email_id = doc.email_id,
            is_primary=1,
            ))
        document.append('phone_nos', dict(
            phone = doc.phone,
            is_primary_mobile_no=1,
            ))
        for i in doc.links:
            document.append('links', dict(
                link_doctype = i.link_doctype,
                link_name=i.link_name,
                link_title=i.link_title
                ))
        document.insert(ignore_permissions=True)
        document.save()
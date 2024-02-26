import frappe
import re

def validate_phone_number(doc, actions):
    if doc.mobile_no:
        phone_pattern = r'^(\+91[-\s]?)?[0]?(91)?[6789]\d{9}$'
        if re.match(phone_pattern, doc.mobile_no):
            return
        else:
            frappe.throw("Phone number is not valid.")
    else:
        frappe.throw("Mobile No is Mandatory...")
    if doc.landline_no:
        pattern = re.compile(r'^\d+$')
        if pattern.match(doc.landline_no):
            return
        else:
            frappe.throw("Landline No number is not valid.")


def merge_mobile_no():
    import frappe
    from frappe.model.rename_doc import update_document_title

    duplicate_mob = frappe.db.sql("""
                    select count(name) as count, mobile_no
                    from `tabCustomer`
                    where ifnull(mobile_no, "") != ""
                    group by mobile_no
                    having count(name)>1
                        """, as_dict=1)

    def match_pattern(mobile):
        import re
        phone_pattern = r'^(\+91[-\s]?)?[0]?(91)?[6789]\d{9}$'
        if re.match(phone_pattern, mobile):
            return True
        return

    count=0
    to_merge = []
    for i in duplicate_mob:
        if i.mobile_no and match_pattern(i.mobile_no):
            count += i.count
            to_merge.append(i)
        else:
            frappe.log_error(i)

    frappe.log_error(f"Total Duplicate Count: {count}")
    cnt=0
    for i in to_merge:
        disabled_cust = frappe.get_all("Customer", filters={"disabled":1, "mobile_no":i.mobile_no}, fields=["name", "customer_name"])
        enabled_cust = frappe.get_all("Customer", filters={"disabled":0, "mobile_no":i.mobile_no}, fields=["name", "customer_name"])

        if len(disabled_cust) == i.count:
            frappe.log_error("All customers are Disabled for Mobile ",i.mobile_no, i.count)
            continue
        if len(disabled_cust)+len(enabled_cust) != i.count:
            frappe.log_error("Count Mismatch: ", i, len(disabled_cust), len(enabled_cust))
            continue

        name_to_change = enabled_cust[0]["name"]
        title_to_change = enabled_cust[0]["customer_name"]
        for i in enabled_cust+disabled_cust:
            frappe.log_error(i)
            try:
                update_document_title(doctype="Customer", docname=i["name"], title=title_to_change, name=name_to_change, merge=1, enqueue=0)
                cnt+=1
                if(cnt%10==0):
                    frappe.db.commit()
            except Exception as e:
                frappe.log_error("Failed", i)
                frappe.log_error(f"Merging Error: {i}", e)
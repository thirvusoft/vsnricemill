import frappe
from frappe import _
from erpnext import get_company_currency, get_default_company
from frappe.modules import scrub

def execute(filters={}):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data


def get_columns(filters={}):
    if filters.get("company"):
        currency = get_company_currency(filters["company"])
    else:
        company = get_default_company()
        currency = get_company_currency(company)
    columns = [
		{
			"label": _("GL Entry"),
			"fieldname": "gl_entry",
			"fieldtype": "Link",
			"options": "GL Entry",
			"hidden": 1,
		},
         {"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 150},
         {"label": _("Voucher Type"), "fieldname": "doc_type", "width": 150, "hidden":1},
		{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
       
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "doc_type",
            "width": 180,
        },
             {
            "label": _("Party Type"),
            "fieldname": "party_type",
            "fieldtype": "Link",
            "options": "Party Type",
            "width": 180,
            "hidden":1
        },
        {
            "label": _("Party"),
            "fieldname": "party",
            "fieldtype": "Dynamic Link",
            "options": "party_type",
            "width": 180,
        },
        {
            "label": _("Mobile No"),
            "fieldname": "mobile_no",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": _("Account Head"),
            "fieldname": "account_head",
            "fieldtype": "Data",
            "width": 180,
        },
		{
			"label": _("Debit ({0})").format(currency),
			"fieldname": "debit",
			"fieldtype": "Float",
			"width": 150,
		},
		{
			"label": _("Credit ({0})").format(currency),
			"fieldname": "credit",
			"fieldtype": "Float",
			"width": 150,
		},
	]
    mode_of_payment_list=frappe.get_all("Mode of Payment",{'name':['Not In',['Debit/Credit Card','Cheque','Bank Draft']]},pluck="name")
    for i in mode_of_payment_list:
        columns.append(
            {"label": i, "fieldtype": "Float", "fieldname": frappe.scrub(i), "width": 150}
        )
    columns.append({"label": _("Remarks"),"fieldname": "remarks","fieldtype": "Small Text","width": 650})
    return columns

def get_data(filters={}):
    si_data = []
    pi_data = []
    pe_data = []
    je_data = []
    final_data = []
    if(filters.get('party_type')):
        if(filters.get('party_type') == 'Customer'):
            si_data = get_sales_invoice_data(filters)
    else:
        si_data = get_sales_invoice_data(filters)

    if(filters.get('party_type')):
        if(filters.get('party_type') == 'Supplier'):
            pi_data = get_purchase_invoice_data(filters)
    else:
        pi_data = get_purchase_invoice_data(filters)

    pe_data = get_payment_entry_data(filters)
    je_data = get_journal_entry_data(filters)

    final_data = si_data + pi_data + pe_data + je_data
    # final_data += [{'credit':sum([i['credit'] for i in final_data if i.get('is_total')]), 'debit':sum([i['debit'] for i in final_data if i.get('is_total')])}]
    # final_data += [{'party':'<b>In Hand (Debit - Credit)</b>','debit':sum([i['debit'] for i in final_data if i.get('is_total')]) - sum([i['credit'] for i in final_data if i.get('is_total')])}]
    return final_data
def get_sales_invoice_data(filters={}):
    # default_receivable_acc = frappe.db.get_value('Company', filters.get('company'), 'default_receivable_account')
    conditions = f'''si.docstatus = 1 '''
    
    if(filters.get('company')):
        conditions += f''' and si.company = '{filters['company']}' '''
    if(filters.get('party')):
        conditions += f''' and si.company in ('{"', '".join(filters['party'])}') '''
    if(filters.get('voucher_no')):
        conditions += f''' and  si.name like '%{filters['voucher_no']}%' '''

    if(filters.get('from_date') and filters.get('to_date')):
        conditions += f''' and si.posting_date BETWEEN '{filters['from_date']}' AND '{filters['to_date']}' '''
    elif(filters.get('from_date')):
        conditions += f''' and si.posting_date >= '{filters['from_date']}' '''
    elif(filters.get('to_date')):
        conditions += f''' and si.posting_date <= '{filters['to_date']}' '''
    if(filters.get('sales_type') == "Credit"):
        conditions += f''' and si.is_pos = 0 and si.is_opening = "No" and si.outstanding_amount>0 '''
    if(filters.get('sales_type') == "Retail"):
        conditions += f''' and si.is_pos = 1 and si.is_opening = "No" and (si.rounded_total - si.outstanding_amount)'''
    # if(filters.get('sales_type') == "Opening"):
    #     conditions += f''' and si.is_opening = "Yes" and si.outstanding_amount>0 and si.is_pos = 0'''        
    if(filters.get('branch')):
        conditions += f''' and si.branch = "{filters['branch']}"  '''
    

    sales_invoices = frappe.db.sql(f"""
        SELECT si.posting_date, si.customer as party, si.name as voucher_no , (si.rounded_total - si.outstanding_amount) as debit, si.outstanding_amount as credit, si.is_pos, (Select mobile_no from `tabCustomer` where name = si.customer) as mobile_no
        FROM `tabSales Invoice` si
        WHERE {conditions}
         ORDER BY si.posting_date;
    """, as_dict = 1)
    for index, i in enumerate(sales_invoices):
        sales_doc=frappe.get_doc("Sales Invoice",i["voucher_no"])
        if sales_doc.payments:
            for j in sales_doc.payments:                
                sales_invoices[index][scrub(j.mode_of_payment)]=j.amount
        i['indent'] = 1
    mode_of_payment_list=frappe.get_all("Mode of Payment",pluck="name")
    total = [{**{scrub(i):0 for i in mode_of_payment_list}, 'indent':1, 'party':"<b>Total Amount</b>", 'debit': sum([i['debit'] for i in sales_invoices]), 'credit': sum([i['credit'] for i in sales_invoices])}]
    
    for i in mode_of_payment_list:
        for m in sales_invoices:
            if(m.get(scrub(i))):
                if(scrub(i) not in total[0]):
                    total[0][scrub(i)] =m.get(scrub(i))
                else:
                    total[0][scrub(i)] +=m.get(scrub(i))
            else:
                m[scrub(i)] = 0
    if(len(sales_invoices) == 0):
        sales_invoices = [{'voucher_no':'No record found', 'indent':1}]
        for i in mode_of_payment_list:
            for j in sales_invoices:
                sales_invoices[0][scrub(i)]=0
    return [{'indent':0, 'voucher_type':'Sales Invoice', 'credit':0, 'debit':0, **{scrub(i):0 for i in mode_of_payment_list}}] + sales_invoices + total
    
def get_purchase_invoice_data(filters={}):
    default_payable_acc = frappe.db.get_value('Company', filters.get('company'), 'default_payable_account')
    conditions = f'''account = '{default_payable_acc}' and voucher_type = 'Purchase Invoice' and party_type = 'Supplier' and credit>0  and is_cancelled = 0 '''

    if(filters.get('company')):
        conditions += f''' and company = '{filters['company']}' '''
    if(filters.get('party')):
        conditions += f''' and party in ('{"', '".join(filters['party'])}') '''
    if(filters.get('voucher_no')):
        conditions += f''' and  voucher_no like '%{filters['voucher_no']}%' '''

    if(filters.get('from_date') and filters.get('to_date')):
        conditions += f''' and posting_date between '{filters['from_date']}' AND '{filters['to_date']}' '''
    elif(filters.get('from_date')):
        conditions += f''' and posting_date >= '{filters['from_date']}' '''
    elif(filters.get('to_date')):
        conditions += f''' and posting_date <= '{filters['to_date']}' '''
    

    if(filters.get('branch')):
        conditions += f''' and branch = "{filters['branch']}"  '''
    

    purchase_invoice = frappe.db.sql(f"""
        SELECT name,voucher_type as doc_type,  posting_date, party, party_type, voucher_no, debit, credit, (Select mobile_no from `tabSupplier` where name = gl.party) as mobile_no
        FROM `tabGL Entry` gl
        WHERE {conditions}
         ORDER BY posting_date;
    """, as_dict = 1)
    for i in purchase_invoice:
        i['indent'] = 1
    d = 0
    c = 0
    for m in purchase_invoice:
        d=d+m.debit
        c=c+m.credit
    if(len(purchase_invoice) == 0):
        purchase_invoice = [{'voucher_no':'No record found', 'indent':1}]
    return [{'indent':0, 'voucher_type':'Purchase Invoice', 'credit':0, 'debit':0}] + purchase_invoice + [{'party':'<b>Total Amount</b>', 'debit':d,'credit':c, 'is_total':1}]

def get_payment_entry_data(filters={}):
    default_payable_acc = frappe.db.get_value('Company', filters.get('company'), 'default_payable_account')
    default_receivable_acc = frappe.db.get_value('Company', filters.get('company'), 'default_receivable_account')
    conditions = f'''account in ('{default_payable_acc}', '{default_receivable_acc}') and voucher_type = 'Payment Entry' and is_cancelled = 0 '''

    if(filters.get('company')):
        conditions += f''' and company = '{filters['company']}' '''
    if(filters.get('party')):
        conditions += f''' and party in ('{"', '".join(filters['party'])}') '''
    if(filters.get('voucher_no')):
        conditions += f''' and  voucher_no like '%{filters['voucher_no']}%' '''

    if(filters.get('from_date') and filters.get('to_date')):
        conditions += f''' and posting_date between '{filters['from_date']}' AND '{filters['to_date']}' '''
    elif(filters.get('from_date')):
        conditions += f''' and posting_date >= '{filters['from_date']}' '''
    elif(filters.get('to_date')):
        conditions += f''' and posting_date <= '{filters['to_date']}' '''
    

    if(filters.get('branch')):
        conditions += f''' and branch = "{filters['branch']}"  '''
    
    party_types = frappe.db.sql(f"""
        SELECT 
            DISTINCT gl.party_type
        FROM `tabGL Entry` gl
        WHERE {conditions}
        ORDER BY posting_date;
    """,  as_list = 1)

    get_party_type_query = lambda party_type: f"""
        (Select mobile_no from `tab{party_type}` where name = gl.party limit 1)
    """
    payment_entry = frappe.db.sql(f"""
        SELECT 
            voucher_type as doc_type, 
            name, 
            posting_date, 
            party, 
            party_type, 
            voucher_no, 
            sum(debit) as credit, 
            sum(credit) as debit, 
            remarks, 
            {f'''CASE
                {" ".join([f" when gl.party_type='{p[0]}' then {get_party_type_query(p[0])} " for p in party_types if p])}
            END as mobile_no''' if party_types else "'' as mobile_no"}
        FROM `tabGL Entry` gl
        WHERE {conditions}
         GROUP BY voucher_no
         ORDER BY posting_date;
    """,  as_dict = 1)
    for i in payment_entry:
        i['indent'] = 1
    d = 0
    c = 0
    for m in payment_entry:
        d=d+m.debit
        c=c+m.credit
    if(len(payment_entry) == 0):
        payment_entry = [{'voucher_no':'No record found', 'indent':1}]
    return [{'indent':0, 'voucher_type':'Payment Entry', 'credit':0, 'debit':0}] + payment_entry + [{'party':'<b>Total Amount</b>', 'debit':d,'credit':c, 'is_total':1}]

def get_journal_entry_data(filters = {}):
    conditions = f'''gl.voucher_type = 'Journal Entry'  and gl.is_cancelled = 0 and al.root_type = "Expense" '''

    if(filters.get('company')):
        conditions += f''' and gl.company = '{filters['company']}' '''
    if(filters.get('party')):
        conditions += f''' and gl.party in ('{"', '".join(filters['party'])}') '''
    if(filters.get('voucher_no')):
        conditions += f''' and  gl.voucher_no like '%{filters['voucher_no']}%' '''

    if(filters.get('from_date') and filters.get('to_date')):
        conditions += f''' and gl.posting_date between '{filters['from_date']}' AND '{filters['to_date']}' '''
    elif(filters.get('from_date')):
        conditions += f''' and gl.posting_date >= '{filters['from_date']}' '''
    elif(filters.get('to_date')):
        conditions += f''' and gl.posting_date <= '{filters['to_date']}' '''
    

    if(filters.get('branch')):
        conditions += f''' and gl.branch = "{filters['branch']}"  '''
    

    journal_entry = frappe.db.sql(f"""
        SELECT gl.name, gl.voucher_type as doc_type, gl.posting_date, gl.party, gl.party_type,gl.voucher_no, gl.debit, gl.credit, gl.remarks, gl.account as account_head, (Select mobile_no from `tabCustomer` where name = gl.party) as mobile_no
        FROM `tabGL Entry` gl
        LEFT JOIN `tabAccount` al ON al.name = gl.account
        WHERE {conditions}
         ORDER BY gl.posting_date;
    """,  as_dict = 1)
    for i in journal_entry:
        i['indent'] = 1
    d = 0
    c = 0
    for m in journal_entry:
        d=d+m.debit
        c=c+m.credit
    if(len(journal_entry) == 0):
        journal_entry = [{'voucher_no':'No record found', 'indent':1}]
    return [{'indent':0, 'voucher_type':'Journal Entry', 'credit':0, 'debit':0}] + journal_entry + [{'party':'<b>Total Amount</b>', 'debit':d,'credit':c, 'is_total':1}]
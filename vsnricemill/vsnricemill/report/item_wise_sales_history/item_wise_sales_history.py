# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data=get_data(filters)
	return columns, data

def get_columns():
    columns = [
        {
            "label": ("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Link",
            "options" : "Item",
            "width": 250
		},
        {
            "label": ("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 250
		},
        {
            "label": ("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 250
		},
    ]
    return columns

def get_data(filters={}):
		data = []
		condition = ""
		if (filters.get('branch')):
			condition += f" AND si.branch = '{filters.get('branch')}'"
		sales_history = f"""
		SELECT sii.item_name as item_name, SUM(sii.qty) as qty, SUM(sii.amount) as amount
		FROM `tabSales Invoice` si
		LEFT JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
		WHERE si.docstatus != 2 
		AND si.is_pos = 1
		AND si.company = '{filters.get('company')}'
		AND si.posting_date BETWEEN '{filters.get('posting_date')}' AND '{filters.get('to_date')}'
		{condition}
		GROUP BY sii.item_name;
	"""
		data=frappe.db.sql(sales_history, as_list=True, debug=1)
		return data
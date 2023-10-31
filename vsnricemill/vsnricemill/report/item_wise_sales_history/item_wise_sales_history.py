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
		{
            "label": ("Type"),
            "fieldname": "type",
            "fieldtype": "Data",
            "width": 100
		}
    ]
    return columns

def get_data(filters={}):
		
		data = []

		condition = ""
		
		if (filters.get('branch')):
			condition += f" AND si.branch = '{filters.get('branch')}'"

		if filters.get('type') == "Retail":
			condition += f" AND si.is_pos = 1"

		if filters.get('type') == "Credit":
			condition += f" AND si.is_pos = 0"

		if filters.get('type'):
			sales_history = f"""
				SELECT
					sii.item_name as item_name, SUM(sii.qty) as qty, SUM(sii.amount) as amount,

				CASE
					WHEN si.is_pos = 1 THEN 'Retail' ELSE 'Credit'
				
				END AS
					type

				FROM 
					`tabSales Invoice` si

				LEFT JOIN 
					`tabSales Invoice Item` sii ON sii.parent = si.name

				WHERE 
					si.docstatus != 2 
					AND si.company = '{filters.get('company')}'
					AND si.posting_date BETWEEN '{filters.get('posting_date')}' AND '{filters.get('to_date')}'
					{condition}

				GROUP BY sii.item_name;
			"""

			data = frappe.db.sql(sales_history, as_list=True)
			
		else:

			sales_history_retail = f"""
				SELECT
					sii.item_name as item_name, SUM(sii.qty) as qty, SUM(sii.amount) as amount,

				CASE
					WHEN si.is_pos = 1 THEN 'Retail' ELSE 'Credit'
				
				END AS
					type

				FROM
					`tabSales Invoice` si

				LEFT JOIN
					`tabSales Invoice Item` sii ON sii.parent = si.name

				WHERE
					si.docstatus != 2
					AND si.is_pos = 1
					AND si.company = '{filters.get('company')}'
					AND si.posting_date BETWEEN '{filters.get('posting_date')}' AND '{filters.get('to_date')}'
					{condition}

				GROUP BY sii.item_name;
			"""

			sales_history_credit = f"""
				SELECT
					sii.item_name as item_name, SUM(sii.qty) as qty, SUM(sii.amount) as amount,

				CASE
					WHEN si.is_pos = 1 THEN 'Retail' ELSE 'Credit'
				
				END AS
					type

				FROM
					`tabSales Invoice` si

				LEFT JOIN
					`tabSales Invoice Item` sii ON sii.parent = si.name

				WHERE
					si.docstatus != 2
					AND si.is_pos = 0
					AND si.company = '{filters.get('company')}'
					AND si.posting_date BETWEEN '{filters.get('posting_date')}' AND '{filters.get('to_date')}'
					{condition}
					
				GROUP BY sii.item_name;
			"""
			
			data = frappe.db.sql(sales_history_retail, as_list=True)

			sales_history_credit = frappe.db.sql(sales_history_credit, as_list=True)

			if sales_history_credit:
				data += sales_history_credit

			data = sorted(data, key=lambda x:(x[0]),reverse=False)

		return data
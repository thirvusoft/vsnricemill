# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta
from frappe import _
from dateutil.relativedelta import relativedelta
month_dict = {

}

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_data(filters):
	
	start_date = filters.get('from_date')
	end_date = filters.get('to_date')

	months_between = get_months_between_dates(start_date, end_date)
	data = []
	result = get_sales_transactions_based_on_customers_or_suppliers(filters)
	previous = frappe.get_all(
					'GL Entry',
					fields=["SUM(credit) as credit", "SUM(debit) as debit", 'posting_date','party'],
					filters={
						"docstatus": 1,
						"company": filters["company"],
						'party': filters.get('customer'),
						'party_type':"Customer",
						"posting_date": ["<", filters["from_date"]],
					},
					group_by='party',
				)
	closing_credit  = 0
	closing_debit = 0
	closing_balance = 0

	data.append({
		'month':'<b>Opening Balance</b>',
		'credit':f'{previous[0].get("credit") if previous else 0}',
		'debit':f'{previous[0].get("debit") if previous else 0}',
		'closing':f'{(previous[0].get("debit") - previous[0].get("credit")) if previous else 0}'
	})	
	closing_balance += (previous[0].get('debit') - previous[0].get('credit')) if previous else 0
	closing_credit += previous[0].get('credit') if previous else 0
	closing_debit += previous[0].get('debit') if previous else 0

	closing = (previous[0].get('debit') - previous[0].get('credit')) if previous else 0

	for mon in months_between:
		row = {}
		row.update({
			'month':mon,
			'credit':result.get(mon)[0] if result.get(mon) else 0,
			'debit':result.get(mon)[1] if result.get(mon) else 0,
			'closing':(result.get(mon)[2] + closing) if result.get(mon) else 0
		})
		closing = row.get('closing')
		closing_balance += row.get('closing')
		closing_credit += row.get('credit')
		closing_debit += row.get('debit')
		data.append(row)
	
	data.append({'month':"<b>Closing Balance</b>",'credit':f'{closing_credit}','debit':f'{closing_debit}','balance':f'{closing_balance}'})
	return data

def get_sales_transactions_based_on_customers_or_suppliers(filters):

		# Fetch the data
		entries = frappe.get_all(
			'GL Entry',
			fields=["SUM(credit) as credit", "SUM(debit) as debit", 'posting_date','party'],
			filters={
				"docstatus": 1,
				"company": filters["company"],
				'party': filters.get('customer'),
				'party_type':"Customer",
				"posting_date": ["between", [filters["from_date"], filters["to_date"]]],
			},
			group_by='posting_date',
		)
		
		# Process the data and format the dates
		result = {}
		for entry in entries:
			credit = entry.credit
			debit = entry.debit

			month_name = entry.posting_date.strftime("%b").upper()
			year = entry.posting_date.strftime("%Y")
			if f"{month_name} {year}" in result:
				result[f"{month_name} {year}"][0] += credit
				result[f"{month_name} {year}"][1] += debit
				result[f"{month_name} {year}"][2] += debit-credit


			else:
				result[f"{month_name} {year}"] = [credit,debit,debit-credit]


		return result
	
def get_columns(filters):
	columns = [
		{
			"label": _("Month"),
			"fieldname": "month",
			"fieldtype": "Data",
			'width':'280px'
		},
		{
			"label": _("Credit"),
			"fieldname": "credit",
			"fieldtype": "Currency",
			'width':'280px'
		},
		{
			"label": _("Debit"),
			"fieldname": "debit",
			"fieldtype": "Currency",
			'width':'280px'
		},
		{
			"label": _("Closing"),
			"fieldname": "closing",
			"fieldtype": "Currency",
			'width':'280px'
		}
	]
	return columns

def get_months_between_dates(start_date, end_date):
	start_date = datetime.strptime(start_date, "%Y-%m-%d")
	end_date = datetime.strptime(end_date, "%Y-%m-%d")
	
	months = []
	while start_date <= end_date:
		month_name = start_date.strftime("%b").upper()
		year = start_date.strftime("%Y")
		months.append(f"{month_name} {year}")
		
		# Increment the month using relativedelta
		start_date += relativedelta(months=1)
		month_dict.update({
			f"{month_name} {year}":{start_date.strftime('%Y-%m')}
		})
	return months
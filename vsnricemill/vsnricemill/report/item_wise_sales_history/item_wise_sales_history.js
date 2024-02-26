// // Copyright (c) 2023, Thirvusoft and contributors
// // For license information, please see license.txt
// /* eslint-disable */

// frappe.query_reports["Item Wise Sales History"] = {
// 	"filters": [
// 		{
// 			"fieldname":"branch",
// 			"label": __("Branch"),
// 			"fieldtype": "Link",
// 			"options": "Branch",
// 		},
// 		{
// 			"fieldname":"company",
// 			"label": __("Company"),
// 			"fieldtype": "Link",
// 			"options": "Company",
// 			"reqd": 1,
            
// 		},
// 		{
// 			"fieldname":"posting_date",
// 			"label": __("From Date"),
// 			"fieldtype": "Date",
// 			"default": "Today",
// 		},
// 		{
// 			"fieldname":"to_date",
// 			"label": __("To Date"),
// 			"fieldtype": "Date",
// 			"default": "Today",
// 		},
// 		{
// 			"fieldname":"type",
// 			"label": __("Type"),
// 			"fieldtype": "Select",
// 			"options": "\nRetail\nCredit",
// 		}
// 	]
// };

// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Item Wise Sales History"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd":1,
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": "\nRetail\nCredit",
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	}
}

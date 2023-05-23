// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Consolidated Day Book"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_permissions()['Company']?frappe.defaults.get_user_permissions()['Company'][0].doc:'',
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "60px"
		},
		{
			"fieldname":"voucher_no",
			"label": __("Voucher No"),
			"fieldtype": "Data",
			on_change: function() {
				frappe.query_report.set_filter_value('group_by', "Group by Voucher (Consolidated)");
			}
		},
		{
			"fieldtype": "Break",
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "Party Type",
			"default": "",
			on_change: function() {
				frappe.query_report.set_filter_value('party', "");
			}
		},
		{
			"fieldname":"party",
			"label": __("Party"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value('party_type');
				if (!party_type) return;

				return frappe.db.get_link_options(party_type, txt);
			},
			on_change: function() {
				var party_type = frappe.query_report.get_filter_value('party_type');
				var parties = frappe.query_report.get_filter_value('party');

				if(!party_type || parties.length === 0 || parties.length > 1) {
					frappe.query_report.set_filter_value('party_name', "");
					frappe.query_report.set_filter_value('tax_id', "");
					return;
				} else {
					var party = parties[0];
					var fieldname = erpnext.utils.get_party_name(party_type) || "name";
					frappe.db.get_value(party_type, party, fieldname, function(value) {
						frappe.query_report.set_filter_value('party_name', value[fieldname]);
					});

					if (party_type === "Customer" || party_type === "Supplier") {
						frappe.db.get_value(party_type, party, "tax_id", function(value) {
							frappe.query_report.set_filter_value('tax_id', value["tax_id"]);
						});
					}
				}
			}
		},
		{
			"fieldname":"party_name",
			"label": __("Party Name"),
			"fieldtype": "Data",
			"hidden": 1
		},
		{
			'fieldname':'branch',
			'label':'Branch',
			'fieldtype':'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options("Branch", txt, {
					company: frappe.query_report.get_filter_value("company")
				});
			},
			// 'hidden':frappe.defaults.get_user_permissions()['Branch']?1:0,
		}
				
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if(data && data.voucher_no =='No record found'){
			value = "<i>" + value + "</i>";
		}
		if (data && data.indent == 0) {
			data.credit = '';
			data.debit = '';
			value = "<b>" + value + "</b>";
		}
		return value;
	},
};

setTimeout(()=>{
	frappe.query_report.set_filter_value('branch', frappe.defaults.get_user_permissions()['Branch']?frappe.defaults.get_user_permissions()['Branch'][0].doc:'') 
	if(frappe.defaults.get_user_permissions()['Branch']){
		document.querySelector('div[data-fieldname="branch"]').classList.add('hidden') 
	}
},100)

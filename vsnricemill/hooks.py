from . import __version__ as app_version

app_name = "vsnricemill"
app_title = "Vsnricemill"
app_publisher = "Thirvusoft"
app_description = "Rice Mill"
app_email = "thirvusoft@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vsnricemill/css/vsnricemill.css"
# app_include_js = "/assets/vsnricemill/js/vsnricemill.js"

# include js, css files in header of web template
# web_include_css = "/assets/vsnricemill/css/vsnricemill.css"
# web_include_js = "/assets/vsnricemill/js/vsnricemill.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vsnricemill/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Invoice" : "/vsnricemill/custom/js/sales_invoice.js",
    "Payment Entry": "/vsnricemill/custom/js/payment_entry.js",
	'Customer': "/vsnricemill/custom/js/customer.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "vsnricemill.utils.jinja_methods",
#	"filters": "vsnricemill.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vsnricemill.install.before_install"
after_install = "vsnricemill.install.after_install"
after_migrate = "vsnricemill.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "vsnricemill.uninstall.before_uninstall"
# after_uninstall = "vsnricemill.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vsnricemill.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Sales Invoice": "vsnricemill.vsnricemill.custom.py.sales_invoice.vsnsalesInvoice",
    
}
# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Item":{
      "validate":"vsnricemill.vsnricemill.custom.py.item.print_name"  
	},
	"Sales Invoice": {
		"autoname": ["vsnricemill.vsnricemill.custom.py.sales_invoice.auto_name",
               		 "vsnricemill.vsnricemill.custom.py.sales_invoice.is_opening_name",
                     "vsnricemill.vsnricemill.custom.py.sales_invoice.counter_sales"],
        "validate" : ["vsnricemill.vsnricemill.custom.py.sales_invoice.validate",
                      "vsnricemill.vsnricemill.custom.py.sales_invoice.loyalty_validate",
                      "vsnricemill.vsnricemill.custom.py.sales_invoice.tax_validate",
					  "vsnricemill.vsnricemill.custom.py.sales_invoice.customer_outstanding_amount"
					   ],
        "on_update_after_submit"  :  "vsnricemill.vsnricemill.custom.py.sales_invoice.customer_outstanding_amount",
        "before_submit" : "vsnricemill.vsnricemill.custom.py.sales_invoice.customer_outstanding_amount",
		# "on_submit" : "vsnricemill.vsnricemill.custom.py.sales_invoice.denomination_on_load",
		# "on_cancel" : "vsnricemill.vsnricemill.custom.py.sales_invoice.cancel_denomination"
	},
    "Payment Entry": {
    	"validate" : 	["vsnricemill.vsnricemill.custom.py.payment_entry.update",
                    "vsnricemill.vsnricemill.custom.py.payment_entry.current_outstanding_amount"
					],
        "before_submit":    "vsnricemill.vsnricemill.custom.py.payment_entry.current_outstanding_amount"
	},
    "Journal Entry" : {
		"validate" : "vsnricemill.vsnricemill.custom.py.journal_entry.update"
	},
    "Customer" : {
        "validate" :"vsnricemill.vsnricemill.custom.py.customer.validate_phone_number"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"vsnricemill.vsnricemill.custom.py.customer.merge_mobile_no"
	]
}

# Testing
# -------

# before_tests = "vsnricemill.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "vsnricemill.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "vsnricemill.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vsnricemill.utils.before_request"]
# after_request = ["vsnricemill.utils.after_request"]

# Job Events
# ----------
# before_job = ["vsnricemill.utils.before_job"]
# after_job = ["vsnricemill.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"vsnricemill.auth.validate"
# ]

from . import __version__ as app_version

app_name = "company_restriction"
app_title = "Company Restriction"
app_publisher = "Your Name"
app_description = "Restrict users to specific companies in ERPNext"
app_email = "your@email.com"
app_license = "MIT"

import frappe

def get_restricted_company():
    user = frappe.session.user
    if user == "Administrator":
        return None
    restricted = frappe.get_value("User", user, "restrict_to_company")
    if not restricted:
        return None
    return frappe.get_value("User", user, "allowed_company")


def get_company_filter(doctype):
    company = get_restricted_company()
    if not company:
        return ""
    if not frappe.db.has_column(doctype, "company"):
        return ""
    return f"`tab{doctype}`.company = '{company}'"


def get_user_filter():
    user = frappe.session.user
    if user == "Administrator":
        return ""
    company = get_restricted_company()
    if company:
        return f"`tabUser`.name = '{user}' OR `tabUser`.restrict_to_company = 0 OR `tabUser`.allowed_company = '{company}'"
    return ""


def has_company_permission(doc, perm):
    if not doc:
        return True
    company = get_restricted_company()
    if not company:
        return True
    if hasattr(doc, "company") and doc.company:
        return doc.company == company
    if doc.doctype == "User":
        if doc.name == frappe.session.user:
            return True
        if frappe.get_value("User", doc.name, "restrict_to_company"):
            return frappe.get_value("User", doc.name, "allowed_company") == company
        return True
    return True


# Permission query conditions
permission_query_conditions = {
    "Company": get_company_filter,
    "Customer": get_company_filter,
    "Supplier": get_company_filter,
    "Item": get_company_filter,
    "Sales Order": get_company_filter,
    "Purchase Order": get_company_filter,
    "Purchase Receipt": get_company_filter,
    "Delivery Note": get_company_filter,
    "Sales Invoice": get_company_filter,
    "Purchase Invoice": get_company_filter,
    "Journal Entry": get_company_filter,
    "Payment Entry": get_company_filter,
    "Stock Entry": get_company_filter,
    "Stock Reconciliation": get_company_filter,
    "GL Entry": get_company_filter,
    "Stock Ledger Entry": get_company_filter,
    "Account": get_company_filter,
    "Cost Center": get_company_filter,
    "Workflow": get_company_filter,
    "Server Script": get_company_filter,
    "Client Script": get_company_filter,
    "User": get_user_filter,
    # Add more doctypes as needed
}

has_permission = {
    "Company": "company_restriction.hooks.has_company_permission",
    "Customer": "company_restriction.hooks.has_company_permission",
    "Supplier": "company_restriction.hooks.has_company_permission",
    "Item": "company_restriction.hooks.has_company_permission",
    "Sales Order": "company_restriction.hooks.has_company_permission",
    "Purchase Order": "company_restriction.hooks.has_company_permission",
    "Purchase Receipt": "company_restriction.hooks.has_company_permission",
    "Delivery Note": "company_restriction.hooks.has_company_permission",
    "Sales Invoice": "company_restriction.hooks.has_company_permission",
    "Purchase Invoice": "company_restriction.hooks.has_company_permission",
    "Journal Entry": "company_restriction.hooks.has_company_permission",
    "Payment Entry": "company_restriction.hooks.has_company_permission",
    "Stock Entry": "company_restriction.hooks.has_company_permission",
    "Stock Reconciliation": "company_restriction.hooks.has_company_permission",
    "GL Entry": "company_restriction.hooks.has_company_permission",
    "Stock Ledger Entry": "company_restriction.hooks.has_company_permission",
    "Account": "company_restriction.hooks.has_company_permission",
    "Cost Center": "company_restriction.hooks.has_company_permission",
    "Workflow": "company_restriction.hooks.has_company_permission",
    "Server Script": "company_restriction.hooks.has_company_permission",
    "Client Script": "company_restriction.hooks.has_company_permission",
    "User": "company_restriction.hooks.has_company_permission",
}
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/company_restriction/css/company_restriction.css"
# app_include_js = "/assets/company_restriction/js/company_restriction.js"

# include js, css files in header of web template
# web_include_css = "/assets/company_restriction/css/company_restriction_web.css"
# web_include_js = "/assets/company_restriction/js/company_restriction_web.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "company_restriction/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
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
#	"methods": "company_restriction.utils.jinja_methods",
#	"filters": "company_restriction.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "company_restriction.install.before_install"
# after_install = "company_restriction.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "company_restriction.uninstall.before_uninstall"
# after_uninstall = "company_restriction.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "company_restriction.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }

# Has Permission
# --------------
# the get_doc method must return a document or None

# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "*": {
        "before_insert": "company_restriction.utils.set_default_company",
        "validate": "company_restriction.utils.validate_company"
    },
    "User": {
        "validate": "company_restriction.utils.validate_user_restriction"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"company_restriction.tasks.all"
#	],
#	"daily": [
#		"company_restriction.tasks.daily"
#	],
#	"hourly": [
#		"company_restriction.tasks.hourly"
#	],
#	"weekly": [
#		"company_restriction.tasks.weekly"
#	]
#	"monthly": [
#		"company_restriction.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "company_restriction.testing.before_tests"

# Overriding Methods
# ------------------------------
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "company_restriction.event.get_events"
# }
#
# each overriding function accepts a `data` parameter;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task" : "company_restriction.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"company_restriction.auth.validate"
# ]
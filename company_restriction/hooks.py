from company_restriction.__version__ import __version__ as app_version

app_name = "company-restriction"
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

# Document Events
doc_events = {
    "*": {
        "before_insert": "company_restriction.utils.set_default_company",
        "validate": "company_restriction.utils.validate_company"
    },
    "User": {
        "validate": "company_restriction.utils.validate_user_restriction"
    }
}
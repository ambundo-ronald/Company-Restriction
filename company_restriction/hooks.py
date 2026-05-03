app_name = "company_restriction"
app_title = "Company Restriction"
app_publisher = "Your Name"
app_description = "Restrict users to specific companies in ERPNext"
app_email = "your@email.com"
app_license = "MIT"

import frappe
from company_restriction.__version__ import __version__ as app_version


fixtures = [
    "Custom Field",
    "Client Script",
]


def get_restricted_company(user=None):
    user = user or frappe.session.user
    if user == "Administrator":
        return None
    restricted = frappe.get_value("User", user, "restrict_to_company")
    if not restricted:
        return None
    return frappe.get_value("User", user, "allowed_company")


def _has_company_field(doctype):
    try:
        return frappe.db.has_column(doctype, "company")
    except Exception:
        return False


def get_company_filter(doctype, user=None):
    company = get_restricted_company(user)
    if not company:
        return ""
    if doctype == "Company":
        return f"`tabCompany`.`name` = {frappe.db.escape(company)}"
    if not _has_company_field(doctype):
        return ""
    return f"`tab{doctype}`.`company` = {frappe.db.escape(company)}"


def get_user_filter(user=None):
    user = user or frappe.session.user
    if user == "Administrator":
        return ""
    company = get_restricted_company(user)
    if company:
        return (
            f"(`tabUser`.`name` = {frappe.db.escape(user)} "
            "OR `tabUser`.`restrict_to_company` = 0 "
            f"OR `tabUser`.`allowed_company` = {frappe.db.escape(company)})"
        )
    return ""


def has_company_permission(doc, user=None, permission_type=None):
    if not doc:
        return True
    user = user or frappe.session.user
    company = get_restricted_company(user)
    if not company:
        return True
    if doc.doctype == "Company":
        return doc.name == company
    if doc.doctype == "User":
        if doc.name == user:
            return True
        if frappe.get_value("User", doc.name, "restrict_to_company"):
            return frappe.get_value("User", doc.name, "allowed_company") == company
        return True
    if getattr(doc, "company", None):
        return doc.company == company
    return True


def get_company_permission_query_conditions(user=None):
    return get_company_filter("Company", user)


def get_customer_permission_query_conditions(user=None):
    return get_company_filter("Customer", user)


def get_supplier_permission_query_conditions(user=None):
    return get_company_filter("Supplier", user)


def get_item_permission_query_conditions(user=None):
    return get_company_filter("Item", user)


def get_sales_order_permission_query_conditions(user=None):
    return get_company_filter("Sales Order", user)


def get_purchase_order_permission_query_conditions(user=None):
    return get_company_filter("Purchase Order", user)


def get_purchase_receipt_permission_query_conditions(user=None):
    return get_company_filter("Purchase Receipt", user)


def get_delivery_note_permission_query_conditions(user=None):
    return get_company_filter("Delivery Note", user)


def get_sales_invoice_permission_query_conditions(user=None):
    return get_company_filter("Sales Invoice", user)


def get_purchase_invoice_permission_query_conditions(user=None):
    return get_company_filter("Purchase Invoice", user)


def get_journal_entry_permission_query_conditions(user=None):
    return get_company_filter("Journal Entry", user)


def get_payment_entry_permission_query_conditions(user=None):
    return get_company_filter("Payment Entry", user)


def get_stock_entry_permission_query_conditions(user=None):
    return get_company_filter("Stock Entry", user)


def get_stock_reconciliation_permission_query_conditions(user=None):
    return get_company_filter("Stock Reconciliation", user)


def get_gl_entry_permission_query_conditions(user=None):
    return get_company_filter("GL Entry", user)


def get_stock_ledger_entry_permission_query_conditions(user=None):
    return get_company_filter("Stock Ledger Entry", user)


def get_account_permission_query_conditions(user=None):
    return get_company_filter("Account", user)


def get_cost_center_permission_query_conditions(user=None):
    return get_company_filter("Cost Center", user)


def get_workflow_permission_query_conditions(user=None):
    return get_company_filter("Workflow", user)


def get_server_script_permission_query_conditions(user=None):
    return get_company_filter("Server Script", user)


def get_client_script_permission_query_conditions(user=None):
    return get_company_filter("Client Script", user)


permission_query_conditions = {
    "Company": "company_restriction.hooks.get_company_permission_query_conditions",
    "Customer": "company_restriction.hooks.get_customer_permission_query_conditions",
    "Supplier": "company_restriction.hooks.get_supplier_permission_query_conditions",
    "Item": "company_restriction.hooks.get_item_permission_query_conditions",
    "Sales Order": "company_restriction.hooks.get_sales_order_permission_query_conditions",
    "Purchase Order": "company_restriction.hooks.get_purchase_order_permission_query_conditions",
    "Purchase Receipt": "company_restriction.hooks.get_purchase_receipt_permission_query_conditions",
    "Delivery Note": "company_restriction.hooks.get_delivery_note_permission_query_conditions",
    "Sales Invoice": "company_restriction.hooks.get_sales_invoice_permission_query_conditions",
    "Purchase Invoice": "company_restriction.hooks.get_purchase_invoice_permission_query_conditions",
    "Journal Entry": "company_restriction.hooks.get_journal_entry_permission_query_conditions",
    "Payment Entry": "company_restriction.hooks.get_payment_entry_permission_query_conditions",
    "Stock Entry": "company_restriction.hooks.get_stock_entry_permission_query_conditions",
    "Stock Reconciliation": "company_restriction.hooks.get_stock_reconciliation_permission_query_conditions",
    "GL Entry": "company_restriction.hooks.get_gl_entry_permission_query_conditions",
    "Stock Ledger Entry": "company_restriction.hooks.get_stock_ledger_entry_permission_query_conditions",
    "Account": "company_restriction.hooks.get_account_permission_query_conditions",
    "Cost Center": "company_restriction.hooks.get_cost_center_permission_query_conditions",
    "Workflow": "company_restriction.hooks.get_workflow_permission_query_conditions",
    "Server Script": "company_restriction.hooks.get_server_script_permission_query_conditions",
    "Client Script": "company_restriction.hooks.get_client_script_permission_query_conditions",
    "User": "company_restriction.hooks.get_user_filter",
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

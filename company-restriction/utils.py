import frappe


def set_default_company(doc, method):
    if hasattr(doc, 'company') and not doc.company:
        user = frappe.session.user
        if user != "Administrator":
            restricted = frappe.get_value("User", user, "restrict_to_company")
            if restricted:
                company = frappe.get_value("User", user, "allowed_company")
                if company:
                    doc.company = company


def validate_company(doc, method):
    if frappe.session.user == "Administrator":
        return
    restricted = frappe.get_value("User", frappe.session.user, "restrict_to_company")
    if not restricted:
        return
    company = frappe.get_value("User", frappe.session.user, "allowed_company")
    if not company:
        return
    if hasattr(doc, 'company') and doc.company and doc.company != company:
        frappe.throw(
            "You are not allowed to create or modify records for another company.",
            frappe.PermissionError,
        )


def validate_user_restriction(doc, method):
    if frappe.session.user == "Administrator":
        return
    if "System Manager" not in frappe.get_roles(frappe.session.user):
        if doc.restrict_to_company or doc.allowed_company:
            frappe.throw("Only System Manager can modify company restriction settings.")

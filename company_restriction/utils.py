import frappe


def _has_field(doc, fieldname):
    meta = getattr(doc, "meta", None)
    if meta and meta.has_field(fieldname):
        return True
    return hasattr(doc, fieldname)


def set_default_company(doc, method):
    if not _has_field(doc, "company") or doc.get("company"):
        return
    user = frappe.session.user
    if user == "Administrator":
        return
    restricted = frappe.get_value("User", user, "restrict_to_company")
    if not restricted:
        return
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
    if _has_field(doc, "company") and doc.get("company") and doc.company != company:
        frappe.throw(
            "You are not allowed to create or modify records for another company.",
            frappe.PermissionError,
        )


def validate_user_restriction(doc, method):
    if frappe.session.user == "Administrator":
        return
    if "System Manager" not in frappe.get_roles(frappe.session.user):
        changed_restriction = (
            doc.is_new()
            or doc.has_value_changed("restrict_to_company")
            or doc.has_value_changed("allowed_company")
        )
        if changed_restriction and (
            doc.get("restrict_to_company") or doc.get("allowed_company")
        ):
            frappe.throw("Only System Manager can modify company restriction settings.")

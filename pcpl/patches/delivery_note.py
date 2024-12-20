import frappe


def execute():
    delivery_notes = frappe.get_list("Delivery Note", filters={"status": "Cancelled"}, fields=["name"])
    for doc in delivery_notes:
         frappe.db.set_value("Delivery Note", doc.name, "custom_advance_received", 0.0)
    frappe.db.commit() # nosemgrep
        
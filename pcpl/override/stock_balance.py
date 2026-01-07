import frappe
from erpnext.controllers.stock_controller import create_repost_item_valuation_entry

def repost_actual_qty(item_code, warehouse, allow_zero_rate=False, allow_negative_stock=False):
    first_sle = frappe.db.sql(
        """
        SELECT posting_date, posting_time
        FROM `tabStock Ledger Entry`
        WHERE item_code=%s AND warehouse=%s AND is_cancelled=0
        ORDER BY posting_date ASC, posting_time ASC, creation ASC
        LIMIT 1
        """,
        (item_code, warehouse),
    )

    posting_date = first_sle[0][0] if first_sle else "1900-01-01"
    posting_time = first_sle[0][1] if first_sle and first_sle[0][1] else "00:01"

    create_repost_item_valuation_entry(
        {
            "item_code": item_code,
            "warehouse": warehouse,
            "posting_date": posting_date,
            "posting_time": posting_time,
            "allow_negative_stock": allow_negative_stock,
            "allow_zero_rate": allow_zero_rate,
        }
    )
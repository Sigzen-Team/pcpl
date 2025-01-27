# Copyright (c) 2025, STPL and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = [
        _('Month') + ':Data:130',
        _('Pending Order amount') + ':Currency:180',
        _('Delivered but not Billed') + ':Currency:180',
        _('Billed Amount') + ':Currency:150',
        _('Total') + ':Currency:150',
    ]

    financial_year = filters.get("financial_year") if filters else None
    year_start_date = frappe.db.get_value("Fiscal Year", {'name': financial_year}, ['year_start_date'])
    year_end_date = frappe.db.get_value("Fiscal Year", {'name': financial_year}, ['year_end_date'])

    month_names = [
        'April', 'May', 'June', 'July', 'August', 'September', 
        'October', 'November', 'December', 'January', 'February', 'March'
    ]

    # Map months from April to March
    month_mapping = list(range(4, 13)) + list(range(1, 4))

    # Query for Pending Orders
    pending_orders = frappe.db.sql("""
        SELECT
        MONTH(so.transaction_date) AS month,
        SUM(soi.base_amount - (soi.billed_amt * IFNULL(so.conversion_rate, 1))) AS total
    FROM
        `tabSales Order` so,
        `tabSales Order Item` soi
    LEFT JOIN `tabSales Invoice Item` sii
        ON sii.so_detail = soi.name AND sii.docstatus = 1
    WHERE
        soi.parent = so.name
        AND so.status = "To Deliver and Bill"
        AND so.docstatus = 1
        AND so.transaction_date BETWEEN %s AND %s
    GROUP BY MONTH(so.transaction_date)
    """,(year_start_date, year_end_date), as_dict=True) # // nosemgrep

    # Query for Delivered but not Billed
    delivered_not_billed = frappe.db.sql("""
        SELECT 
            MONTH(posting_date) AS month, 
            SUM(
                CASE 
                    WHEN currency = 'USD' OR (currency = 'INR' AND price_list_currency = 'USD') THEN base_rounded_total 
                    ELSE total 
                END
            ) AS total
        FROM `tabDelivery Note`
        WHERE status = 'To Bill'
        AND posting_date BETWEEN %s AND %s
        GROUP BY MONTH(posting_date)
    """, (year_start_date, year_end_date), as_dict=True)# // nosemgrep

    # Query for Billed Amounts
    billed_amounts = frappe.db.sql("""
        SELECT 
            MONTH(posting_date) AS month, 
            SUM(
                CASE 
                    WHEN currency = 'USD' OR (currency = 'INR' AND price_list_currency = 'USD') THEN base_rounded_total 
                    ELSE total 
                END
            ) AS total
        FROM `tabSales Invoice`
        WHERE status NOT IN ('Cancelled', 'Draft')
        AND posting_date BETWEEN %s AND %s
        GROUP BY MONTH(posting_date)
    """, (year_start_date, year_end_date), as_dict=True)# // nosemgrep

    data = []
    for mapped_month in month_mapping:
        pending = next((item.total for item in pending_orders if item.month == mapped_month), 0)
        delivered = next((item.total for item in delivered_not_billed if item.month == mapped_month), 0)
        billed = next((item.total for item in billed_amounts if item.month == mapped_month), 0)
        total = pending + delivered + billed
        month_index = month_mapping.index(mapped_month)
        data.append([month_names[month_index], pending, delivered, billed, total])

    return columns, data


// Copyright (c) 2025, STPL and contributors
// For license information, please see license.txt

frappe.query_reports["Monthly Sales and Delivery Report"] = {
	"filters": [
        {
            "fieldname": "financial_year",
            "label": __("Financial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            "reqd": 1
        }
    ]
};

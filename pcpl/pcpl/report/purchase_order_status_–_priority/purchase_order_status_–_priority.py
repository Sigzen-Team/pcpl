# Copyright (c) 2026, STPL and contributors
# For license information, please see license.txt



import frappe

def execute(filters=None):
	columns = [
		{"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 90},
		{"label": "Purchase Order", "fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order", "width": 130},
		{"label": "Supplier", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 200},
		{"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 70},
		{"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 100},
		{"label": "Received Qty", "fieldname": "received_qty", "fieldtype": "Float", "width": 120},
		{"label": "Qty to Receive", "fieldname": "qty_to_receive", "fieldtype": "Float", "width": 130},
		{"label": "Expected Date", "fieldname": "expected_date", "fieldtype": "Date", "width": 100},
		{"label": "Status", "fieldname": "po_status", "fieldtype": "Data", "width": 150},
		{"label": "Followup Date", "fieldname": "followup_date", "fieldtype": "Date", "width": 110},
		{"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
		{"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 120},
		{"label": "Order Status", "fieldname": "order_status", "fieldtype": "Data", "width": 120},
	]

	data = frappe.db.sql("""
		SELECT 
			po.transaction_date AS date,
			po.name AS purchase_order,
			po.supplier,
			poi.item_code,
			poi.uom,
			poi.qty,
			poi.received_qty,
			(poi.qty - IFNULL(poi.received_qty,0)) AS qty_to_receive,
			poi.expected_delivery_date AS expected_date,
			po.po_status,
			po.po_status_update_date AS followup_date,
			poi.priority,
			poi.item_group,
			po.status AS order_status
		FROM `tabPurchase Order` po
		INNER JOIN `tabPurchase Order Item` poi
			ON poi.parent = po.name
		WHERE 
			po.docstatus < 2
			AND po.status NOT IN ("Stopped","Closed")
			AND IFNULL(poi.received_qty,0) < IFNULL(poi.qty,0)
		ORDER BY po.transaction_date ASC
	""", as_dict=1)

	return columns, data
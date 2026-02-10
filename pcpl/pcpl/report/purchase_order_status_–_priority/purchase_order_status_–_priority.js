// Copyright (c) 2026, STPL and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase order status – Priority"] = {
	"filters": [

	],
	
	formatter: function(value, row, column, data, default_formatter) {

		// default format
		value = default_formatter(value, row, column, data);
	
		// Apply color ONLY to Priority column
		if (data && data.priority === "Urgent" && column.fieldname === "priority") {
			value = `<span style="
						background-color:#ffe6e6;
						color:#b30000;
						font-weight:bold;
						padding:3px 6px;
						border-radius:4px;">
						${value}
					 </span>`;
		}
	
		return value;
	}
};

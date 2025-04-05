// Copyright (c) 2025, Natnael Abrham and contributors
// For license information, please see license.txt

frappe.query_reports["Profit & Loss Analysis"] = {
	filters: [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Datetime",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Datetime",
		},
	],
};

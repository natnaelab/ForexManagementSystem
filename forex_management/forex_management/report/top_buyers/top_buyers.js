// Copyright (c) 2025, Natnael Abrham and contributors
// For license information, please see license.txt

frappe.query_reports["Top Buyers"] = {
	filters: [
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "currency",
			label: __("Currency"),
			fieldtype: "Link",
			options: "FXCurrency",
		},
		{
			fieldname: "since_from",
			label: __("Since from"),
			fieldtype: "Datetime",
		},
		{
			fieldname: "to_date",
			label: __("To"),
			fieldtype: "Datetime",
		},
	],
};

// Copyright (c) 2025, Natnael Abrham and contributors
// For license information, please see license.txt

frappe.query_reports["Top Currencies"] = {
	filters: [
		{
			fieldname: "currency",
			label: __("Currency"),
			fieldtype: "Link",
			options: "FXCurrency",
		},
	],
};

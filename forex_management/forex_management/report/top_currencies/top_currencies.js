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
		{
			fieldname: "transaction_type",
			label: __("Transaction Type"),
			fieldtype: "Select",
			options: "\nBuy\nSell",
			default: "",
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

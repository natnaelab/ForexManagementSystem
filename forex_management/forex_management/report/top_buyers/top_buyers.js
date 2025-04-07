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
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Datetime",
			reqd: 1,
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Datetime",
			reqd: 1,
			default: frappe.datetime.now_datetime(),
		},
	],
};

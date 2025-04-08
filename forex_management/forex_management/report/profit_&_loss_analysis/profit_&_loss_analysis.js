// Copyright (c) 2025, Natnael Abrham and contributors
// For license information, please see license.txt

frappe.query_reports["Profit & Loss Analysis"] = {
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
			options: "Currency"
		},
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			options: "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
			default: new Date().toLocaleString('default', { month: 'long' })
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Datetime",
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Datetime",
			reqd: 1
		},
	],

onload(report) {
	const today = new Date()
	const monthName = today.toLocaleString('default', { month: 'long' })

	report.set_filter_value("month", monthName)

	const fromDate = new Date(today.getFullYear(), today.getMonth(), 1)
	const toDate = new Date(today.getFullYear(), today.getMonth() + 1, 0)
	report.set_filter_value("from_date", frappe.datetime.get_datetime_as_string(fromDate))
	report.set_filter_value("to_date", frappe.datetime.get_datetime_as_string(toDate))

	const monthMap = {
		January: 0, February: 1, March: 2, April: 3, May: 4, June: 5,
		July: 6, August: 7, September: 8, October: 9, November: 10, December: 11
	};

	report.get_filter('month').$input.on('change', function () {
		const selected = $(this).val();
		const now = new Date();
		const year = now.getFullYear();
		let fromDate = new Date(year, now.getMonth(), 1);
		let toDate = new Date(year, now.getMonth() + 1, 0);

		if (selected && monthMap[selected] !== undefined) {
			const monthIndex = monthMap[selected];
			fromDate = new Date(year, monthIndex, 1);
			toDate = new Date(year, monthIndex + 1, 0);
		}

		frappe.query_report.set_filter_value('from_date', frappe.datetime.get_datetime_as_string(fromDate));
		frappe.query_report.set_filter_value('to_date', frappe.datetime.get_datetime_as_string(toDate));
	});

	report.get_filter('to_date').$input.on('change', function () {
		const from = frappe.query_report.get_filter_value('from_date');
		var [y, m, d] = from.split(" ")[0].split("-").map(Number)
		const fromDate = new Date(y, m, d);

		const to = $(this).val();
		var [d, m, y] = to.split(" ")[0].split("-").map(Number)
		const toDate = new Date(y, m, d)

		if (!from || !to) return;

		if (fromDate > toDate)
			return frappe.throw("'To date' filter cannot be lower than 'From date'");
	});
},
};

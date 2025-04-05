# Copyright (c) 2025, Natnael Abrham and contributors
# For license information, please see license.txt

# import frappe
from frappe import _
import frappe


def execute(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """
    columns = get_columns()
    data = get_data(filters=filters)
    chart = get_chart(filters=filters)
    summary_report = get_summary_report(filters=filters)

    return columns, data, None, chart, summary_report


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Data", "width": "150"},
        {
            "label": _("Amount (ETB) Bought"),
            "fieldname": "amount_bought",
            "fieldtype": "Value",
        },
        {
            "label": _("Amount (ETB) Sold"),
            "fieldname": "amount_sold",
            "fieldtype": "Value",
        },
        {
            "label": _("P&L"),
            "fieldname": "profit_loss",
            "fieldtype": "Value",
        },
    ]


def get_data(filters: dict | None) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    filter_opts = {}
    if filters.get("customer"):
        filter_opts["customer"] = filters["customer"]

    if filters.get("from_date") and filters.get("to_date"):
        filter_opts["date_and_time"] = ["between", [filters["from_date"], filters["to_date"]]]
    elif filters.get("from_date"):
        filter_opts["date_and_time"] = [">=", filters["from_date"]]
    elif filters.get("to_date"):
        filter_opts["date_and_time"] = ["<", filters["to_date"]]

    transactions = frappe.db.get_all(
        "Transaction",
        filters=filter_opts,
        fields=[
            "customer_name",
            "exchange_rate",
            "SUM(IF(transaction_type = 'Buy', amount, 0)) as amount_bought",
            "SUM(IF(transaction_type = 'Sell', amount, 0)) as amount_sold",
            "SUM(amount) as total_amount",
        ],
        order_by="total_amount desc",
        group_by="customer",
    )

    data = []
    for transaction in transactions:
        profit_loss = transaction.amount_sold - transaction.amount_bought

        data.append(
            {
                "customer": transaction.customer_name,
                "amount_bought": f"{transaction.amount_bought:,.2f}",
                "amount_sold": f"{transaction.amount_sold:,.2f}",
                "profit_loss": f"{profit_loss:,.2f}",
            }
        )

    return data


def get_chart(filters: dict | None) -> dict:
    all_data = get_data(filters=filters)
    labels = [row["customer"] for row in all_data]
    amount_bought = [float(row["amount_bought"].replace(",", "")) for row in all_data]
    amount_sold = [float(row["amount_sold"].replace(",", "")) for row in all_data]
    profit_loss = [float(row["profit_loss"].replace(",", "")) for row in all_data]

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": _("Bought"), "values": amount_bought},
                {"name": _("Sold"), "values": amount_sold},
                {"name": _("Profit/Loss"), "values": profit_loss},
            ],
        },
        "type": "bar",
    }


def get_summary_report(filters) -> dict:
    filter_opts = {}

    if filters.get("customer"):
        filter_opts["customer"] = filters["customer"]

    if filters.get("from_date") and filters.get("to_date"):
        filter_opts["date_and_time"] = ["between", [filters["from_date"], filters["to_date"]]]
    elif filters.get("from_date"):
        filter_opts["date_and_time"] = [">=", filters["from_date"]]
    elif filters.get("to_date"):
        filter_opts["date_and_time"] = ["<", filters["to_date"]]

    transactions = frappe.db.get_all(
        "Transaction",
        filters=filter_opts,
        fields=[
            "SUM(IF(transaction_type = 'Buy', amount, 0)) as amount_bought",
            "SUM(IF(transaction_type = 'Sell', amount, 0)) as amount_sold",
        ],
    )
    total_amount_bought = transactions[0].amount_bought if transactions else 0
    total_amount_sold = transactions[0].amount_sold if transactions else 0

    return [
        {
            "label": _("Total Amount Bought"),
            "value": f"{total_amount_bought:,.2f}",
            "indicator": "green",
            "description": _("Total amount bought."),
            "color": "#10B981",
        },
        {
            "label": _("Total Amount Sold"),
            "value": f"{total_amount_sold:,.2f}",
            "indicator": "red",
            "description": _("Total amount sold."),
            "color": "#EF4444",
        },
    ]

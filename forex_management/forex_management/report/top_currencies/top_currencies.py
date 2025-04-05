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
        {
            "fieldname": "currency",
            "label": _("Currency"),
            "fieldtype": "Data",
            "options": "Currency",
            "width": 200,
        },
        {
            "fieldname": "amount_bought",
            "label": _("Amount Bought"),
            "fieldtype": "Value",
            "options": "Amount Bought",
        },
        {
            "fieldname": "amount_sold",
            "label": _("Amount Sold"),
            "fieldtype": "Value",
            "options": "Amount Sold",
        },
    ]


def get_data(filters: dict | None) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

    filter_opts = {}

    if filters.get("currency"):
        filter_opts["currency"] = filters.get("currency")

    if filters.get("transaction_type"):
        filter_opts["transaction_type"] = filters.get("transaction_type")

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
            "currency",
            "SUM(IF(transaction_type = 'Buy', amount, 0)) as amount_bought",
            "SUM(IF(transaction_type = 'SELL', amount, 0)) as amount_sold",
            "SUM(amount) as total_amount",
        ],
        order_by="total_amount desc",
        group_by="currency",
    )

    data = []

    for transaction in transactions:
        data.append(
            {
                "currency": f"{transaction.currency}",
                "amount_bought": f"{transaction.amount_bought:,.2f}",
                "amount_sold": f"{transaction.amount_sold:,.2f}",
            },
        )

    return data


def get_chart(filters: dict | None) -> dict:
    all_data = get_data(filters=filters)
    labels = [row["currency"] for row in all_data]

    amount_bought = [float(row["amount_bought"].replace(",", "")) for row in all_data]
    amount_sold = [float(row["amount_sold"].replace(",", "")) for row in all_data]

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": _("Bought"), "values": amount_bought},
                {"name": _("Sold"), "values": amount_sold},
            ],
        },
        "type": "bar",
        "colors": ["#10B981", "#EF4444"],
    }


def get_summary_report(filters: dict | None) -> dict:
    def _get_most_traded_currency(transaction_type):
        filter_opts = {}

        if filters.get("currency"):
            filter_opts["currency"] = filters.get("currency")
        if filters.get("transaction_type"):
            filter_opts["transaction_type"] = filters.get("transaction_type")
        if filters.get("from_date"):
            filter_opts["date_and_time"] = [">=", filters.get("from_date")]
        if filters.get("to_date"):
            filter_opts["date_and_time"] = ["<", filters.get("to_date")]

        filter_opts["transaction_type"] = transaction_type

        most_traded_currency = frappe.db.get_all(
            "Transaction",
            filters=filter_opts,
            fields=["currency", "SUM(amount) as amount"],
            order_by="amount desc",
            group_by="currency",
            limit=1,
        )
        return most_traded_currency[0] if most_traded_currency else None

    most_bought = _get_most_traded_currency("Buy")
    most_sold = _get_most_traded_currency("Sell")

    most_bought_value = (
        f"{most_bought.get('amount', 0):,.2f} ({most_bought.get('currency', '').split('(')[1].strip(')')})"
        if most_bought
        else "0.00"
    )
    most_sold_value = (
        f"{most_sold.get('amount', 0):,.2f} ({most_sold.get('currency', '').split('(')[1].strip(')')})"
        if most_sold
        else "0.00"
    )

    return [
        {
            "label": _("Most Bought"),
            "value": most_bought_value,
            "indicator": "green",
            "description": _("Most Bought Currency"),
            "color": "#10B981",
        },
        {
            "label": _("Most Sold"),
            "value": most_sold_value,
            "indicator": "red",
            "description": _("Most Sold Currency"),
            "color": "#EF4444",
        },
    ]

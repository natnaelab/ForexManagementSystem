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
    data = get_data()

    return columns, data


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


def get_data() -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

    transactions = frappe.db.get_all(
        "Transaction",
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

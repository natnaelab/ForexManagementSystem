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


def get_data() -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    transactions = frappe.db.get_all(
        "Transaction",
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

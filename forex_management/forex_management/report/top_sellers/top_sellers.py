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

    print(filters)

    columns = get_columns()
    data = get_data(filters=filters)

    return columns, data


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Data",
            "options": "Customer",
            "width": 130,
        },
        {
            "fieldname": "amount_fx",
            "label": _("FX Amount"),
            "fieldtype": "Float",
            "options": None,
            "width": 100,
            "precision": 2,
        },
        {
            "fieldname": "amount_etb",
            "label": _("Amount (ETB)"),
            "fieldtype": "Float",
            "options": None,
            "width": 125,
            "precision": 2,
        },
        {
            "fieldname": "currency",
            "label": _("Currency"),
            "fieldtype": "Data",
            "options": "Currency",
        },
        {
            "fieldname": "exchange_rate",
            "label": _("Rate"),
            "fieldtype": "Float",
            "options": "Exchange Rate",
        },
    ]


def get_data(filters: dict | None) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

    filter_opts = {"transaction_type": "Sell"}

    if filters.get("customer"):
        filter_opts["customer"] = filters["customer"]

    if filters.get("currency"):
        filter_opts["currency"] = filters["currency"]

    if filters.get("since_from"):
        if filters.get("to_date"):
            filter_opts["date_and_time"] = [">=", filters["since_from"], "<", filters["to_date"]]
        filter_opts["date_and_time"] = [">=", filters["since_from"]]

    transactions = frappe.db.get_all(
        "Transaction",
        filters=filter_opts,
        fields=["customer_name", "currency", "exchange_rate", "SUM(amount) as total_amount"],
        order_by="total_amount desc",
        group_by="customer",
    )

    data = []
    for transaction in transactions:
        amount_etb = transaction.total_amount * transaction.exchange_rate

        data.append(
            {
                "customer": transaction.customer_name,
                "amount_fx": transaction.total_amount,
                "amount_etb": amount_etb,
                "currency": transaction.currency,
                "exchange_rate": transaction.exchange_rate,
            }
        )

    return data

# Copyright (c) 2025, Natnael Abrham and contributors
# For license information, please see license.txt

# import frappe
from frappe import _


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
            "label": "Sell Transaction",
            "fieldname": "sell_tx",
            "fieldtype": "Link",
            "options": "Transaction",
            "width": 150,
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 120,
        },
        {
            "label": "Currency",
            "fieldname": "currency",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "Sell Amount",
            "fieldname": "amount",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": "Sell Rate",
            "fieldname": "exchange_rate",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": "Total PnL",
            "fieldname": "pnl",
            "fieldtype": "Currency",
            "width": 120,
        },
        {
            "label": "Date",
            "fieldname": "time",
            "fieldtype": "Datetime",
            "width": 150,
        },
    ]


def get_data(filters: dict | None) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    filter_opts = {"transaction_type": "Sell"}

    if filters.get("customer"):
        filter_opts["customer"] = filters["customer"]

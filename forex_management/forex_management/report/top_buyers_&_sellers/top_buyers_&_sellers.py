# Copyright (c) 2025, Natnael Abrham and contributors
# For license information, please see license.txt

# import frappe
from forex_management.forex_management.report import top_sellers
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
    summary_report = get_summary_report(filters=filters)

    return columns, data, None, None, summary_report


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
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
            "width": 120,
            "precision": 2,
        },
        {
            "fieldname": "currency",
            "label": _("Currency"),
            "fieldtype": "Data",
            "options": "Currency",
            "width": 200,
        },
        {
            "fieldname": "exchange_rate",
            "label": _("Rate"),
            "fieldtype": "Float",
            "options": "Exchange Rate",
        },
        {
            "fieldname": "transaction_type",
            "label": _("Type"),
            "fieldtype": "Select",
            "options": "Buy, Sell",
            "width": 80,
        },
    ]


def get_data(filters: dict | None) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

    filter_opts = get_filters(filters) | {"transaction_type": filters.get("transaction_type")}

    transactions = frappe.db.get_all(
        "Transaction",
        filters=filter_opts,
        fields=[
            "customer",
            "currency",
            "exchange_rate",
            "SUM(amount) as total_amount",
            "transaction_type",
        ],
        order_by="total_amount desc",
        group_by="customer,currency,transaction_type",
    )

    data = []
    for transaction in transactions:
        amount_etb = transaction.total_amount * transaction.exchange_rate

        data.append(
            {
                "customer": transaction.customer,
                "amount_fx": transaction.total_amount,
                "amount_etb": amount_etb,
                "currency": transaction.currency,
                "exchange_rate": transaction.exchange_rate,
                "transaction_type": transaction.transaction_type,
            }
        )

    return data


def get_filters(filters: dict | None) -> dict:
    filter_opts = {}

    if filters.get("customer"):
        filter_opts["customer"] = filters["customer"]
    if filters.get("currency"):
        filter_opts["currency"] = filters["currency"]

    if filters.get("from_date") and filters.get("to_date"):
        filter_opts["date_and_time"] = ["between", [filters["from_date"], filters["to_date"]]]
    elif filters.get("from_date"):
        filter_opts["date_and_time"] = [">=", filters["from_date"]]
    elif filters.get("to_date"):
        filter_opts["date_and_time"] = ["<=", filters["to_date"]]

    return filter_opts


def get_summary_report(filters: dict | None) -> dict:
    def _get_top_customer(transaction_type):
        filter_opts = get_filters(filters) | {"transaction_type": transaction_type}

        customer, currency, amount, exchange_rate = frappe.db.get_value(
            "Transaction",
            filters=filter_opts,
            fieldname=["customer", "currency", "amount", "exchange_rate"],
        ) or [{}]

        amount_etb = amount * exchange_rate
        return f"{customer} </br> ({amount_etb:,.2f} ETB)"

    top_buyer = _get_top_customer("Buy")
    top_seller = _get_top_customer("Sell")

    return [
        {
            "label": _("Top Buyer"),
            "value": top_buyer,
            "indicator": "green",
            "description": _("Most Bought Currency"),
            "color": "#10B981",
        },
        {
            "label": _("Top Seller"),
            "value": top_seller,
            "indicator": "red",
            "description": _("Most Sold Currency"),
            "color": "#EF4444",
        },
    ]

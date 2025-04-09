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

    return columns, data, None, chart


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
            "fieldname": "total_fee_collected",
            "label": _("Total Fee Collected"),
            "fieldtype": "Currency",
            "width": 160,
        },
        {
            "fieldname": "total_transactions",
            "label": _("Total Transactions"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "buy_count",
            "label": _("Buy Count"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "sell_count",
            "label": _("Sell Count"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "total_buy_amount",
            "label": _("Total Buy Amount"),
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "fieldname": "total_sell_amount",
            "label": _("Total Sell Amount"),
            "fieldtype": "Float",
            "width": 150,
        },
    ]


def get_data(filters: dict | None) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

    filter_opts = {}

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
            "currency.currency_name",
            "exchange_rate",
            "COUNT(CASE WHEN transaction_type = 'Buy' THEN 1 END) as buy_count",
            "COUNT(CASE WHEN transaction_type = 'Sell' THEN 1 END) as sell_count",
            "COUNT(amount) as total_tx_count",
            "SUM(IF(transaction_type = 'Buy', amount, 0)) as amount_bought",
            "SUM(IF(transaction_type = 'Sell', amount, 0)) as amount_sold",
        ],
        group_by="currency",
    )

    for transaction in transactions:
        transaction["fee"] = (transaction.amount_bought + transaction.amount_sold) * transaction.exchange_rate * 0.005

    transactions = sorted(transactions, key=lambda tx: tx.get("fee"), reverse=True)

    data = []
    for transaction in transactions:
        data.append(
            {
                "currency": transaction.currency_name,
                "total_transactions": transaction.total_tx_count,
                "buy_count": transaction.buy_count,
                "sell_count": transaction.sell_count,
                "total_fee_collected": transaction.fee,
                "total_buy_amount": transaction.amount_bought,
                "total_sell_amount": transaction.amount_sold,
            }
        )

    return data


def get_chart(filters: dict | None) -> dict:
    all_data = get_data(filters=filters)
    labels = [row["currency"] for row in all_data]

    total_fee = [row["total_fee_collected"] for row in all_data]

    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": _("Bought"), "values": total_fee}],
        },
        "type": "bar",
        "colors": ["#10B981"],
    }

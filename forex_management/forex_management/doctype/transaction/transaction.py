# Copyright (c) 2025, Natnael Abrham and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType


class Transaction(Document):
    def autoname(self):
        self.name = f"{self.currency.split('(')[1].replace(')', '')}/ETB - Amount: {self.amount}"


@frappe.whitelist()
def get_active_currencies(doctype, txt, searchfield, start, page_len, filters):
    currencies = frappe.db.get_all("FXCurrency", fields=[searchfield], filters={"is_active": 1})

    return [(currency["name"], currency["name"]) for currency in currencies]

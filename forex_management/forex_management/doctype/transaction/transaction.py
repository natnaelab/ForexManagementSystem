# Copyright (c) 2025, Natnael Abrham and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries


class Transaction(Document):
    def autoname(self):
        series_number = getseries("", 3)
        selected_currency = frappe.get_value("FXCurrency", {"name": self.currency}, "currency_code")
        base_currency_code = "ETB" if self.transaction_type == "Buy" else selected_currency
        target_currency_code = selected_currency if self.transaction_type == "Buy" else "ETB"
        self.name = f"TX{series_number} - {target_currency_code}/{base_currency_code} - Amount: {self.amount}"

    def before_insert(self):
        self.amount_etb = float(self.amount) * float(self.exchange_rate)

    def on_submit(self):
        if self.transaction_type != "Sell":
            return

        remaining_to_match = self.amount

        buys = frappe.db.get_all(
            "Transaction",
            filters={"customer": self.customer, "currency": self.currency, "transaction_type": "Buy"},
            fields=["amount", "amount_sold", "exchange_rate", "name"],
        )

        for buy in buys:
            if remaining_to_match <= 0:
                break

            available = buy.amount - (buy.amount_sold or 0)
            if available <= 0:
                continue

            matched_amount = min(available, remaining_to_match)
            pnl = matched_amount * (float(self.exchange_rate) - buy.exchange_rate)

            self.append(
                "linked_buys",
                {
                    "buy_transaction": buy.name,
                    "matched_amount": matched_amount,
                    "buy_exchange_rate": buy.exchange_rate,
                    "pnl": pnl,
                },
            )

            frappe.db.set_value("Transaction", buy.name, "amount_sold", (buy.amount_sold or 0) + matched_amount)

            remaining_to_match -= matched_amount

        if remaining_to_match > 0:
            frappe.throw("Not enough balance for selected currency to complete this transaction.")

    def validate(self):
        if self.transaction_type == "Sell":
            total_available = 0
            remaining_to_sell = self.amount

            buys = frappe.db.get_all(
                "Transaction",
                filters={"customer": self.customer, "currency": self.currency, "transaction_type": "Buy"},
                fields=["amount", "amount_sold", "exchange_rate"],
                order_by="creation ASC",
            )
            print(buys)
            for buy in buys:
                total_available += buy.amount - (buy.amount_sold or 0)
                if total_available >= remaining_to_sell:
                    break

            if total_available < remaining_to_sell:
                frappe.throw(f"You don't have enough {self.currency} to sell!")


@frappe.whitelist()
def get_active_currencies(doctype, txt, searchfield, start, page_len, filters):
    currencies = frappe.db.get_all("FXCurrency", fields=[searchfield], filters={"is_active": 1})

    return [(currency["name"], currency["name"]) for currency in currencies]

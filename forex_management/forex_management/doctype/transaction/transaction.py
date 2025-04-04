# Copyright (c) 2025, Natnael Abrham and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Transaction(Document):
	def autoname(self):
		self.name = f"{self.currency.split('(')[1].replace(')', '')}/ETB - Amount: {self.amount}"

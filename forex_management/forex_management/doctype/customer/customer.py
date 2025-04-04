# Copyright (c) 2025, Natnael Abrham and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Customer(Document):
    def get_full_name(self):
        self.first_name = self.first_name.strip().title()
        if self.last_name:
            self.last_name = self.last_name.strip().title()

        return f"{self.first_name} {self.last_name or ''}".strip().title()

    def before_save(self):
        self.full_name = self.get_full_name()

    def autoname(self):
        self.name = self.get_full_name()

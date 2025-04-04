// Copyright (c) 2025, Natnael Abrham and contributors
// For license information, please see license.txt


const genRandomExchangeRate = () => {
    return (Math.random() * (135 - 137) + 137).toFixed(4);
};



frappe.ui.form.on("Transaction", {
    refresh(frm) { },

    before_load(frm) {
        rate = genRandomExchangeRate();
        frm.set_value("exchange_rate", rate);
    }
});

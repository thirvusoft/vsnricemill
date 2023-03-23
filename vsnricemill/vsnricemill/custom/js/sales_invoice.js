frappe.ui.form.on("Sales Invoice", {
    refresh: function (frm, cdt, cdn) {
        frm.set_query("brand_name", "items", function (f, cdt, cdn) {
            let data = locals[cdt][cdn]
            return {
                filters: {
                    "item_name": data.item_name,
                    "item_code": ["!=", data.item_code]
                }

            }
        })

    }
})

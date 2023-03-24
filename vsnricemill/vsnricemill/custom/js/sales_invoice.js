frappe.ui.form.on("Sales Invoice Item", {
    item_code: function(frm,cdt,cdn){
        var row = locals[cdt][cdn]
        frappe.call({
            
            method: "vsnricemill.vsnricemill.custom.py.sales_invoice.get_attribute",
            args:{
                items:row,
            },

            callback: function(r) {
                frappe.model.set_value(cdt,cdn,"size",r.message)
                  
        }
        })
    },
})

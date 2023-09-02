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
frappe.ui.form.on("Sales Invoice", {
    customer: function(frm,cdt,cdn){
                frappe.call({
                    method: "vsnricemill.vsnricemill.custom.py.sales_invoice.loyalty",
                    args:{
                        customer:frm.doc.customer,
                        company:frm.doc.company
                    },
                    callback: function(r) {
                        frm.set_value("existing_loyalty_point",r.message)
                }
                })
                frappe.call({
                    method: "vsnricemill.vsnricemill.custom.py.sales_invoice.customer_advance_amount",
                    args:{
                        customer:frm.doc.customer,
                        
                    },
                    callback: function(r) {
                       if (r.message[0]["total_unpaid"] < 0){
                        let text = r.message[0]["total_unpaid"]
                        let amount = `<p style="color:Tomato;font-size:15px;">
						Advance Amount ${text}
                        </p>`
                    frm.set_df_property('advance_amount', 'options', amount);

                       }
                       else{
                        let amount = `<p style="color:Tomato;font-size:15px;">
						Advance Amount ${0}
                        </p>`
                    frm.set_df_property('advance_amount', 'options', amount);
                       }
                      
                }
                })
            
            }
    
})
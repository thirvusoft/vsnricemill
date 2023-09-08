frappe.ui.form.on("Sales Invoice Item", {
    item_code: function(frm,cdt,cdn){
        if(frm.doc.is_return){
            frm.events.apply_loose_item_filter(frm)
        }
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
    refresh: function(frm){
        if(frm.doc.is_return){
            frm.events.apply_loose_item_filter(frm)
        }
        if(!frm.is_new()){
            frm.events.get_advance_amount(frm)
        }
    },
    is_return: function(frm){
        if(frm.doc.is_return){
            frm.events.apply_loose_item_filter(frm)
        }
        else{
            frm.events.remove_loose_item_filter(frm)
        }
    },
    company: function(frm){
            frm.events.get_advance_amount(frm)
    },
    customer: function(frm){
        frm.events.get_advance_amount(frm)
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
    },
    apply_loose_item_filter: function(frm){
        frm.set_query("item_code", "items", ()=>{
            return {
                query: "erpnext.controllers.queries.item_query",
                filters:{
                    'is_sales_item': 1, 
                    'customer': frm.doc.customer, 
                    'has_variants': 0,
                    'company':frm.doc.company,
                    'is_loose_item_for_return':1
                } 
            }
        })
    },
    remove_loose_item_filter: function(frm){
        frm.set_query("item_code", "items", ()=>{
            return {
                query: "erpnext.controllers.queries.item_query",
                filters:{
                    'is_sales_item': 1, 
                    'customer': frm.doc.customer, 
                    'has_variants': 0,
                    'company':frm.doc.company,
                } 
            }
        })
    },
    get_advance_amount:function(frm){
        frappe.call({
            method: "vsnricemill.vsnricemill.custom.py.sales_invoice.customer_advance_amount",
            args:{
                customer:frm.doc.customer,
                company:frm.doc.company
                
            },
            callback: function(r) {
                if(!r.message){
                    frm.set_df_property('advance_amount', 'options', `<p style="color:Tomato;font-size:15px;">
                    Advance Amount ${fmt_money(0)}
                    </p>`);
                    return
                }
               if (r.message[0]["total_unpaid"] < 0){
                let text = r.message[0]["total_unpaid"] * -1
                let amount = `<p style="color:Tomato;font-size:15px;">
                Advance Amount ${fmt_money(text)}
                </p>`
            frm.set_df_property('advance_amount', 'options', amount);

               }
               else{
                let amount = `<p style="color:Tomato;font-size:15px;">
                Advance Amount ${fmt_money(0)}
                </p>`
            frm.set_df_property('advance_amount', 'options', amount);
               }
              
        }
        })
    }
    
})
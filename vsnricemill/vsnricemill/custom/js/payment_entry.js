frappe.ui.form.on("Payment Entry", {
    refresh:function(frm){
        frm.events.apply_internal_company_filter(frm)
    },
    comapny:function(frm){
        frm.events.apply_internal_company_filter(frm)
    },
    party_type:function(frm){
        frm.events.apply_internal_company_filter(frm)
    },
    apply_internal_company_filter:function(frm){
        if(["Customer", "Supplier"].includes(frm.doc.party_type)){
            frm.set_query("party", ()=>{
                return {
                    filters:{
                        "internal_company":["!=", frm.doc.company]
                    }
                }
            })
        }
        else{
            frm.set_query("party", ()=>{
                return {
                    filters:{

                    }
                }
            })
        }
    }
})
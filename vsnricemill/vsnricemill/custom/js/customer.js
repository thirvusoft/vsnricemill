frappe.ui.form.on("Customer", {
    refresh:function(frm){
        frm.add_custom_button(__('Monthly Breakup'), () => {
            frappe.set_route('query-report', "Monthly Breakup", {customer: frm.doc.name});

        },('View'));
    }

})
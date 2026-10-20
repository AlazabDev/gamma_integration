frappe.ui.form.on("Quotation", {
  refresh(frm) {
    if (frm.is_new()) return;
    frm.add_custom_button(__("Generate AI Proposal"), () => {
      frappe.call({
        method: "gamma_integration.api_foundry.generate_document",
        args: {source_doctype: frm.doctype, source_name: frm.doc.name},
        freeze: true,
        callback(r) {
          if (!r.message || !r.message.proposal) return;
          frappe.msgprint({
            title: __("Generation queued"),
            message: __("Generated document: {0}", [r.message.proposal]),
            indicator: "blue"
          });
        }
      });
    }, __("Gamma"));
  }
});

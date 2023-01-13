from odoo import fields, models


class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_wizard_reason(self):
        wizard_view_id = self.env.ref("payment_reminder.so_cancel_reason_form").id
        print("00000000000000000000000", self.env['sale.order'].browse(self.env.context.get('active_ids')))

        return {
            "name": "so.cancel.reason",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "so.cancel",
            "view_id": wizard_view_id,
            "target": "new",
            "context": {'sale_id': self.env['sale.order'].browse(self.env.context.get('active_ids')).id},
        }

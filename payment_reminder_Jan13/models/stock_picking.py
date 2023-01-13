from odoo import fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    def action_button_validate(self):
        """Opens wizard for
            validation Confirmation on Picking"""
        sp_wizard_view_id = self.env.ref("payment_reminder.sp_lots_serial_form_view").id
        return {
            "name": "Confirm Validation",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "wizard.lots.serial",
            "view_id": sp_wizard_view_id,
            "target": "new",
            "context": {'stock_id': self.id},
        }

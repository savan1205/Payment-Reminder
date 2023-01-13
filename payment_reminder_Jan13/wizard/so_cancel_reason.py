from odoo import fields, models


class CrmLeadLost(models.TransientModel):
    _name = 'so.cancel'
    _description = 'Get cancel Reason'

    lost_reason_id = fields.Many2one("so.lost.reason", string="Lost Reason")

    def action_lost_reason_so(self):
        sale_order = self.env['sale.order'].browse(int(self.env.context.get('sale_id')))
        sale_order.write({
            'lost_reason_id': self.lost_reason_id
        })
        sale_order._action_cancel()

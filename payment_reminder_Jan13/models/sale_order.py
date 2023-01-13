from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_rem_id = fields.Many2one(comodel_name="payment.reminder.config")
    # lost_reason_id = fields.Many2one("so.lost.reason", readonly=True)

    def send_cancellation_mail(self):
        return self.action_quotation_send()
#
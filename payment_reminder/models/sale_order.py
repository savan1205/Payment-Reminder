from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_rem_id = fields.Many2one(comodel_name="payment.reminder.config")

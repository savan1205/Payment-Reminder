from odoo import fields, models, _


class SoLostReason(models.Model):
    _name = "so.lost.reason"
    _description = 'So Lost Reason'

    name = fields.Char('Description', required=True)
    active = fields.Boolean('Active', default=True)

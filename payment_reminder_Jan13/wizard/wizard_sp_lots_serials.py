from odoo import fields, models


class WizardLotsSerial(models.TransientModel):
    _name = "wizard.lots.serial"
    _description = "wizard.lots.serial"

    lots_ids = fields.Text(string="lots_line_ids", readonly=True)

    def default_get(self, fields):
        """Defaultly gets/fills data(product with its Lots/Serial number)
            based on active stock picking lines"""
        res = super(WizardLotsSerial, self).default_get(fields)
        picking_id = self.env['stock.picking'].browse(self.env.context.get('stock_id'))
        add_string = ""
        product_list = []
        for move_lines in picking_id.move_line_ids_without_package:
            if move_lines.product_id not in product_list:
                product_list.append(move_lines.product_id)
                add_string += '\n' + str(move_lines.product_id.name) + ' - ' + str(move_lines.lot_id.name)
            else:
                add_string += ',' + str(move_lines.lot_id.name)
            res.update({
                'lots_ids': add_string
            })
        return res

    def action_button_validate(self):
        return self.env['stock.picking'].browse(self.env.context.get('stock_id')).button_validate()

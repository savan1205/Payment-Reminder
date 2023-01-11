from odoo import api, fields, models, _
from datetime import timedelta, date
from ast import literal_eval

class PaymentReminderConfig(models.Model):
    _name = "payment.reminder.config"

    name = fields.Char(string="name", copy=False, readonly=True, default=lambda self: _('New'))

    def _default_mail_template(self):
        return self.env.ref('payment_reminder.send_payment_reminder_email')

    mail_template_id = fields.Many2one(comodel_name="mail.template", default=_default_mail_template,
                                       string="Mail Template")
    sales_domain = fields.Char(default=[('state', '=', 'sale')],string="sales domain")
    sale_order_ids = fields.One2many(comodel_name="sale.order",
                                     inverse_name="payment_rem_id",
                                     string="sale_order_ids")
    deadline_days = fields.Integer(string="Deadline Days")

    # Methods
    @api.model
    def create(self, vals):
        """Method for Sequence Generation On Records"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'payment.reminder.config') or _('New')
        res = super(PaymentReminderConfig, self).create(vals)
        return res

    def default_get(self,fields):
        sale_order_ids = self.env['sale.order'].search([('state','=','sale')])
        for rec in sale_order_ids:
            if not rec.payment_rem_id:
                rec.payment_rem_id = self._origin
        return super(PaymentReminderConfig,self).default_get(fields)



    def name_get(self):
        """This method will concatenate name and Expiration
           days for Sales Order"""
        result = []
        for rec in self:
            result.append((rec.id, "%s (Expires in %s Days)" % (rec.name, rec.deadline_days)))
        return result

    @api.onchange('sales_domain')
    def get_domain(self):
        '''Automatically fill O2m with Sale Order Records
            on changing domain'''
        # if self.sales_domain:
        domain = literal_eval(self.sales_domain)
        sale_ids = self.env['sale.order'].search(domain)
        for rec in sale_ids:
            if not rec.payment_rem_id:
                rec.payment_rem_id = self._origin

    def sent_mail_cron(self):
        '''Automation/Cron to send reminder mail
            after deadline Days'''
        sale_order_ids = self.env['sale.order'].search([('state', '=', 'sale')])
        for rec in sale_order_ids:
            template_id = rec.payment_rem_id.mail_template_id if rec.payment_rem_id.mail_template_id else self.env.ref(
                'payment_reminder.send_payment_reminder_email')
            deadline_days = rec.payment_rem_id.deadline_days
            req_date = rec.date_order + timedelta(days=deadline_days)
            if req_date.date() == date.today():
                self.env['mail.template'].browse(template_id.id).send_mail(rec.id, force_send=True)
            # Check Payment Status
            exp_date = rec.date_order + timedelta(days = deadline_days+7)
            if date.today() >= exp_date.date():
                for record in rec.invoice_ids:
                    if record.state != 'posted':
                        rec._action_cancel()


from odoo import api, fields, models, _
from datetime import timedelta, date
import ast
from odoo.osv import expression


class PaymentReminderConfig(models.Model):
    _name = "payment.reminder.config"

    name = fields.Char(
        string="name", copy=False, readonly=True, default=lambda self: _("New")
    )

    def _default_mail_template(self):
        return self.env.ref("payment_reminder.send_payment_reminder_email")

    mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        default=_default_mail_template,
        string="Mail Template",
    )
    sales_domain = fields.Char(
        default=[("state", "=", "sale"), ("payment_rem_id", "=", False)],
        string="sales domain",
    )

    def _default_sale_ids(self):
        domain = expression.AND(
            [ast.literal_eval(self.sales_domain or "[]"), [("state", "=", "sale")]]
        )
        sale_quot_ids = self.env["sale.order"].search(domain)
        return sale_quot_ids[0]

    sale_order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="payment_rem_id",
        string="sales order",
        default=_default_sale_ids,
    )
    deadline_days = fields.Integer(string="Deadline Days")

    # Methods
    @api.model
    def create(self, vals):
        """Method for Sequence Generation On Records"""
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "payment.reminder.config"
            ) or _("New")
        res = super(PaymentReminderConfig, self).create(vals)
        return res

    def name_get(self):
        """This method will concatenate name and Expiration
        days for Sales Order"""
        result = []
        for rec in self:
            result.append(
                (rec.id, "%s (Expires in %s Days)" % (rec.name, rec.deadline_days))
            )
        return result

    @api.onchange("sales_domain")
    def get_domain(self):
        """Automatically fill O2m with Sale Order Records
        on changing domain"""
        domain = ast.literal_eval(self.sales_domain)
        sale_ids = self.env["sale.order"].search(domain)
        self.write({"sale_order_ids": [(6, 0, sale_ids.ids)]})

    def sent_mail_cron(self):
        """Automation/Cron to send reminder mail
        after deadline Days"""
        sale_order_ids = self.env["sale.order"].search(
            [("state", "=", "sale"), ("payment_rem_id", "!=", False)]
        )
        for rec in sale_order_ids:
            template_id = (
                rec.payment_rem_id.mail_template_id
                if rec.payment_rem_id.mail_template_id
                else self.env.ref("payment_reminder.send_payment_reminder_email")
            )
            deadline_days = rec.payment_rem_id.deadline_days
            req_date = rec.date_order + timedelta(days=deadline_days)
            if req_date.date() == date.today():
                template_id.send_mail(rec.id, force_send=True)
            # Check Payment Status
            exp_date = rec.date_order + timedelta(days=deadline_days + 7)
            if date.today() >= exp_date.date():
                for record in rec.invoice_ids:
                    if record.state != "posted":
                        rec._action_cancel()

{
    "name": "payment_reminder",
    "version": "15.0.1.0.1",
    "summary": "payment reminder for Sales Order Module",
    "sequence": 1,
    "description": """
        This module contains all the features of Payment reminder in Sales Order.
    """,
    "depends": ["sale_management", "mail"],
    "data": [
        "security/ir.model.access.csv",

        "views/payment_reminder_config_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_filter_pyrm.xml",
        "views/stock_picking_views.xml",
        # "views/so_lost_reason_views.xml",

        "data/pymr_sequence.xml",
        "data/payment_reminder_cron.xml",
        "data/payment_reminder_mail.xml",
        "report/sale_report_inherit.xml",

        "wizard/wizard_sp_lots_serial_views.xml",
        # "wizard/mail_compose_message.xml",
        # "wizard/so_cancel_reason_views.xml",

    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}

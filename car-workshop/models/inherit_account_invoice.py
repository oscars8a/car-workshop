from odoo import api, fields, models
from wdb import set_trace as depurador

class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    description = fields.Html(string="Description")

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    repair_ids = fields.Many2many(comodel_name='car_workshop.repair', relation="repair_purchase")
from odoo import api, fields, models,_



class SaleOrder(models.Model):
    _inherit = "sale.order"

    repair_id = fields.Many2one('car_workshop.repair', string="Repair Order")

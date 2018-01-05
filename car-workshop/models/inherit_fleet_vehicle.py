# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, )
    image_client_vehicle = fields.Binary(string="Car image")

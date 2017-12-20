# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    res_partner = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, )

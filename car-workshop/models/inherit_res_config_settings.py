# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class CarWorkConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    unique_area = fields.Boolean(string="Unique 'Area Repair & Revision'")

    areas_count = fields.Integer()

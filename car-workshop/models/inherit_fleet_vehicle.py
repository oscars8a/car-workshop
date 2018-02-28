# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True, )
    image_client_vehicle = fields.Binary(string="Car image")


    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.model_id and not self.image_client_vehicle:
            self.image_client_vehicle = self.image_medium

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True, )
    image_client_vehicle = fields.Binary(string="Car image")

    repairs_count = fields.Integer('Repairs', compute='_compute_repairs_count')


    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.model_id and not self.image_client_vehicle:
            self.image_client_vehicle = self.image_medium

    def _compute_repairs_count(self):
        repairs_obj = self.env['car_workshop.repair']
        for vehicle in self:
            vehicle.repairs_count = repairs_obj.search_count([
                ('vehicle_id.id', '=', vehicle.id)
            ])
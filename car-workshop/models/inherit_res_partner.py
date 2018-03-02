# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):

    _inherit = 'res.partner'

    vehicles_count = fields.Integer('Vehicles',
                                        compute='_compute_vehicles_count')
    repairs_count = fields.Integer('Repairs', compute='_compute_repairs_count')

    def _compute_vehicles_count(self):
        vehicles_obj = self.env['fleet.vehicle']
        for partner in self:
            partner.vehicles_count = vehicles_obj.search_count([
                ('customer_id.id', '=', partner.id)
            ])

    def _compute_repairs_count(self):
        repairs_obj = self.env['car_workshop.repair']
        for partner in self:
            partner.repairs_count = repairs_obj.search_count([
                ('partner_id.id', '=', partner.id)
            ])

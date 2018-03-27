# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from wdb import set_trace as depurador

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    unique_area_setting = fields.Boolean(string="Unique Area 'Repair and Revision'")
    areas_count = fields.Integer(compute='_compute_areas_count', string="Pruebas")
    module_sdi_unique_area = fields.Boolean(string="PRUEBAS Instalar SDi Unique Area")

    @api.multi
    @api.onchange('unique_area_setting')
    def _compute_areas_count(self):
        for record in self:
            record.areas_count = self.env['project.project'].search_count([('car_work','=',True)])
            if record.areas_count > 1:
                record.unique_area_setting = False

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            unique_area_setting = ICPSudo.get_param('CarWorkshop.unique_area_setting')
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("CarWorkshop.unique_area_setting", self.unique_area_setting)

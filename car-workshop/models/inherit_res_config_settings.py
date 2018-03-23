# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    unique_area_setting = fields.Boolean(string="Unique Area 'Repair and Revision'")

    #Es necesario indicar la forma que vamos a realizar la persistencia.

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
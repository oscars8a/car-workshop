# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Task(models.Model):
    _inherit = 'project.task'

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )

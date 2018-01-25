# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Project(models.Model):
    _inherit = 'project.project'

    car_work = fields.Boolean(string="It's car's work?")


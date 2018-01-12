# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Project(models.Model):
    _inherit = 'project.project'

    car_work = fields.Boolean(string="It's car's work?", default="True")


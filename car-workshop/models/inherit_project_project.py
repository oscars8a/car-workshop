# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Project(models.Model):
    _inherit = 'project.project'

    carwork = fields.Boolean(string="It's carwork", value="True")

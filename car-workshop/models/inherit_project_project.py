# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Project(models.Model):
    _inherit = 'project.project'

    def _compute_repair_count(self):
        task_data = self.env['car_workshop.repair'].read_group([('project_id', 'in', self.ids), '|', ('stage_id.fold', '=', False), ('stage_id', '=', False)], ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.repair_count = result.get(project.id, 0)

    car_work = fields.Boolean(string="It's car's work?")
    repair_count = fields.Integer(compute='_compute_repair_count', string="Repairs")

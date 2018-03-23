# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from wdb import set_trace as depurador

class Project(models.Model):
    _inherit = 'project.project'

    def _compute_repair_count(self):
        task_data = self.env['car_workshop.repair'].read_group([
            ('project_id', 'in', self.ids),
            '|', ('stage_id.fold', '=', False), ('stage_id', '=', False)], ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.repair_count = result.get(project.id, 0)

    car_work = fields.Boolean(string="It's Car's work Area?", default=True)
    repair_count = fields.Integer(compute='_compute_repair_count', string="Repairs")


    @api.model
    def _action_redirect_area(self):
        obj_settings = self.env['res.config.settings']
        kanban_ref = self.env.ref('car-workshop.car-workshop_project_view_kanban').id
        action = {
            "name": "Area",
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "views": [[kanban_ref, "kanban"], [False, "form"], [False, "search"]],
            "domain": [("car_work","=",True)],
            "target": "main",
        }
        print('HI ODOO DEVELOPER')
        print(obj_settings.unique_area_setting)
        if obj_settings.unique_area_setting:
            pass
        return action
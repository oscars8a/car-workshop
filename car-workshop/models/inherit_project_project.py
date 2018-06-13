# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
# from wdb import set_trace as depurador


class Project(models.Model):
    _inherit = 'project.project'

    def _compute_repair_count(self):
        task_data = self.env['car_workshop.repair'].read_group(
            [('finished_stage', '=', False)], ['project_id'], ['project_id'])
        print(task_data)

        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        print(result)

        for project in self:
            project.repair_count = result.get(project.id, 0)

    car_work = fields.Boolean(string="It's Car's work Area?", default=True)
    repair_count = fields.Integer(compute='_compute_repair_count', string="Repairs")
    repair_image = fields.Binary(string="",  )


    # CAMBIARLO POR module_INSTALARMod en el settings, cuando sea estable.
    # Método del Action Server action_prueba_unique_area
    def _action_redirect_area(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        unique_area_value = ICPSudo.get_param('CarWorkshop.unique_area_setting')
        area_ids = self.env['project.project'].search([('car_work','=',True)])
        area_count = len(area_ids)
        areas_kanban_ref = self.env.ref('car-workshop.car-workshop_project_view_kanban').id
        action = {
            "name": _("Areas"),
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "views": [[areas_kanban_ref, "kanban"], [False,"tree"], [False, "form"], [False, "search"]],
            "domain": [("car_work","=",True)],
            "target": "main",
        }
        if unique_area_value and area_count == 1:
            area_id = area_ids[0].id
            repair_kanban_ref = self.env.ref('car-workshop.car-workshop_repair_view_kanban').id
            # Y que pasa cuando queremos traducir estos actios? Los dejamos en inglés? _("Lo que queremos traducir")
            action={
                "name": _("Repairs"),
                "type": "ir.actions.act_window",
                "res_model": "car_workshop.repair",
                "views": [[repair_kanban_ref, "kanban"], [False,"tree"], [False,"calendar"], [False, "form"], [False, "search"]],
                "context":{
                    'group_by': 'stage_id',
                    'search_default_project_id': [area_id],
                    'default_project_id': area_id,
                    'search_default_in_work': 1,
                },
                "target": "current",
            }
        return action
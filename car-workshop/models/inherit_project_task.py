# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Task(models.Model):
    _name = 'car_workshop.repair'

    _inherits = {
        'project.task': 'project_task_id',
        'sale.order': 'sale_order_id',
    }

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    def _compute_task_id(self):
        vals = {'sequence': 10,
                'tag_ids': [[6, False, []]],
                'planned_hours': 0,
                'company_id': 1,
                'stage_id': 8,
                'displayed_image_id': False,
                'user_id': 1,
                'email_from': 'admin@yourcompany.example.com',
                'partner_id': 3,
                'date_deadline': False,
                'active': True,
                'project_id': 7,
                'kanban_state': 'normal',
                'parent_id': False,
                'sale_line_id': False,
                'description': False,
                'email_cc': False,
                'name': 'PRUEBAS HOLA',
                'priority': '0'}
        rec = self.env['project.task'].create(vals)
        print(rec)
        return rec

    project_task_id = fields.Many2one('project.task', required=True, ondelete='cascade', compute=_compute_task_id())
    sale_order_id = fields.Many2one('sale.order', required=True, ondelete='cascade')

    # project_task_id_name = fields.Char(string="", required=False, related='project_task_id.name')
    # sale_order_id_name = fields.Char(string="", required=False, related='sale_order_id.name')


    @api.model
    def create(self, vals):
        rec = super(Task, self).create(vals)
        return rec

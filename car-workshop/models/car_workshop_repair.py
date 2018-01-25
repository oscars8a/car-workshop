# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Repair(models.Model):
    _name = 'car_workshop.repair'
    # _inherit = 'sale.order'

    # Error, a partner cannot follow twice the same object.
    # _inherits = {
    #     'sale.order': 'sale_order_id'
    # }

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    # Error, a partner cannot follow twice the same object.
    sale_order_id = fields.Many2one('sale.order',delegate=True, required=True, ondelete='cascade')



    project_task_id = fields.Many2one('project.task', required=True)
    stage_id = fields.Many2one(related="project_task_id.stage_id", store=True )
    project_id = fields.Many2one(related="project_task_id.project_id", store=True)
    user_id = fields.Many2one(related="project_task_id.user_id", store=True)
    kanban_state = fields.Selection(related="project_task_id.kanban_state", store=True)
    date_start = fields.Datetime(related="project_task_id.date_start", store=True)
    planned_hours = fields.Float(related="project_task_id.planned_hours", store=True)
    date_deadline = fields.Date(related="project_task_id.date_deadline", store=True)

    # timesheet_ids = fields.One2many('account.analytic.line', 'task_id', 'Timesheets')

    # ERROR
    # column "None" appears twice in unique constraint
    # tag_ids = fields.Many2many(related="project_task_id.tag_ids", store=True)


    @api.model
    def create(self, vals):
        print('HI ODOO DEVELOPER !!!!!')
        # print(str(vals))
        # self.sale_order_id.create(vals)
        vals['name']='prueba'
        print('HI ODOO DEVELOPER 2 !!!')
        print(str(vals))
        # No se como asignar el nuevo registro project_task_id a nuetro registro car-workshop.repair
        self.project_task_id.create(vals)
        # print(rec_task)
        # vals['project_task_id'] = rec_task

        print('HI ODOO DEVELOPER 3 !!!')
        print(vals)

        rec = super(Repair, self).create(vals)
        return rec

























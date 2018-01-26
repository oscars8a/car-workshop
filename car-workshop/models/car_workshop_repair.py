# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Repair(models.Model):
    _name = 'car_workshop.repair'

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    sale_order_id = fields.Many2one('sale.order', delegate=True, required=True, ondelete='cascade')

    project_task_id = fields.Many2one('project.task', required=True)
    stage_id = fields.Many2one(related="project_task_id.stage_id")
    project_id = fields.Many2one(related="project_task_id.project_id")
    user_id = fields.Many2one(related="project_task_id.user_id")
    kanban_state = fields.Selection(related="project_task_id.kanban_state")
    date_start = fields.Datetime(related="project_task_id.date_start")
    date_deadline = fields.Date(related="project_task_id.date_deadline")
    tag_ids = fields.Many2many(related="project_task_id.tag_ids")

    # timesheet_ids = fields.One2many('account.analytic.line', 'task_id', 'Timesheets')
    timesheet_ids = fields.One2many(related="project_task_id.timesheet_ids")
    planned_hours = fields.Float(related="project_task_id.planned_hours")
    total_hours_spent = fields.Float(related="project_task_id.total_hours_spent")
    progress = fields.Float(related="project_task_id.progress")
    effective_hours = fields.Float(related="project_task_id.effective_hours")
    children_hours = fields.Float(related="project_task_id.children_hours")
    remaining_hours = fields.Float(related="project_task_id.remaining_hours")


    @api.model
    def create(self, vals):
        print('HI ODOO DEVELOPER ! !!!')
        # vals no contiene el par "name" y como hay que crear primero project.task es necesario añadirlo.
        print('HI ODOO DEVELOPER 1 !!!')
        vals['name'] = 'prueba'
        print(str(vals))
        rec_task = self.project_task_id.create(vals).id
        vals['project_task_id'] = rec_task
        print('HI ODOO DEVELOPER 2 !!!')
        print(vals)
        print('HI ODOO DEVELOPER 3 !!!')
        # rec_timesheets = self.timesheet_ids.create(vals).id
        # vals['timesheet_ids'] = [rec_timesheets]
        print(vals)
        # el valor final de "name" será el que hemos elegido anteriormente, no el precalculado por sale.order
        # IMPORTANTE: las sale.order DEBEN tener un nombre único y calculado?
        rec = super(Repair, self).create(vals)
        return rec


    # Hace falta sobreescribir el metodo delete
    # @api.model
    # def delete(self, vals):
    #

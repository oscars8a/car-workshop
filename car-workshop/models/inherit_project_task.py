# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Task(models.Model):
    _name = 'car_workshop.repair'

    # _inherits = {
    #     'project.task': 'project_task_id',
    #     'sale.order': 'sale_order_id',
    # }

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    project_task_id = fields.Many2one('project.task', delegate=True, required=True, ondelete='cascade')
    sale_order_id = fields.Many2one('sale.order', delegate=True, required=True, ondelete='cascade')

    # project_task_id_name = fields.Char(string="", required=False, related='project_task_id.name')
    # sale_order_id_name = fields.Char(string="", required=False, related='sale_order_id.name')


    @api.model
    def create(self, vals):
        print('HI ODOO DEVELOPER !!!!!')
        print('HI ODOO 222222222')
        rec = super(Task, self).create(vals)
        print('HI ODOO 333333333')
        return rec

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Task(models.Model):
    _name = 'car_workshop.repair'

    # _inherit = 'sale.order'
    # _inherits = {
    #     'project.task': 'project_task_id',
    #     'sale.order': 'sale_order_id',
    # }

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    project_task_id = fields.Many2one('project.task', delegate=True, required=True, ondelete='cascade')
    # sale_order_id = fields.Many2one('sale.order', delegate=True, required=True, ondelete='cascade')


    @api.model
    def create(self, vals):
        print('HI ODOO DEVELOPER !!!!!')
        rec = super(Task, self).create(vals)
        print(rec)
        print('HI ODOO 2222222222')
        return rec

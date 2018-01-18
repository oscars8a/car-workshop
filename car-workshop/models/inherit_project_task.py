# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class Task(models.Model):
    _name = 'car_workshop.repair'


    _inherits = {
        'project.task': 'project_task_id',
        'sale.order': 'sale_order_id',
    }

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    project_task_id = fields.Many2one('project.task', required=True, ondelete='cascade')
    sale_order_id = fields.Many2one('sale.order', required=True, ondelete='cascade')

    # project_task_id_name = fields.Char(string="", required=False, related='project_task_id.name')
    # sale_order_id_name = fields.Char(string="", required=False, related='sale_order_id.name')


    @api.model
    def create(self, vals):
        _logger.debug("HI ODOO DEVELOPER!!!")
        _logger.debug(str(vals))
        # self.project_task_id.create(vals)
        # params = dict(vals)
        # if 'name' in params:
        #     params['name'] = ''
        # self.sale_order_id.create(params)
        rec = super(Task, self).create(vals)
        return rec

    # @api.multi
    # @api.onchange('partner_shipping_id', 'partner_id')
    # def onchange_partner_shipping_id_repair(self):
    #     self.sale_order_id.convert_to_onchange()

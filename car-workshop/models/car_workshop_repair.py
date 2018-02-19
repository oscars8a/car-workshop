# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Repair(models.Model):
    _name = 'car_workshop.repair'

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    sale_order_id = fields.Many2one('sale.order', delegate=True, required=True, ondelete='cascade')

    project_task_id = fields.Many2one('project.task', required=True, ondelete='cascade')
    stage_id = fields.Many2one(related="project_task_id.stage_id", store=True)
    project_id = fields.Many2one(related="project_task_id.project_id", store=True)
    user_id = fields.Many2one(related="project_task_id.user_id")
    kanban_state = fields.Selection(related="project_task_id.kanban_state")
    date_start = fields.Datetime(related="project_task_id.date_start")
    date_deadline = fields.Date(related="project_task_id.date_deadline")
    tag_ids = fields.Many2many(related="project_task_id.tag_ids")
    color = fields.Integer(related="project_task_id.color")
    timesheet_ids = fields.One2many(related="project_task_id.timesheet_ids")
    planned_hours = fields.Float(related="project_task_id.planned_hours")
    total_hours_spent = fields.Float(related="project_task_id.total_hours_spent")
    progress = fields.Float(related="project_task_id.progress")
    effective_hours = fields.Float(related="project_task_id.effective_hours")
    children_hours = fields.Float(related="project_task_id.children_hours")
    remaining_hours = fields.Float(related="project_task_id.remaining_hours")


    @api.model
    def create(self, vals):

        # vals['name'] = 'prueba'
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'sale.order') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')


        rec_task = self.project_task_id.create(vals).id
        vals['project_task_id'] = rec_task

        # IMPORTANTE: las sale.order DEBEN tener un nombre único y calculado?
        rec = super(Repair, self).create(vals)
        return rec


    # Hace falta sobreescribir el metodo delete?
    # @api.model
    # def delete(self, vals):
    #

    # Pasa algo muy raro cuando queremos intalar la app por primera vez, nos da problemas porque no encuentra el form del
    # wizard, ya que se carga despues. Se soluciona cambiando el orden en el manifes.
    # Pero, y no estoy seguro que sea por eso, una vez instalado y creamos un repair nos sale el famoso error follow twice
    # Parece que se arregla volviendo a dejar la vista wizard donde estaba en el manifest
    # Todo esto sin tener el Sales Management instalado.


    def _pruebas_(self):
        print("HOLA MUNDOOOOOOOOO")
        print(self.stage_id)

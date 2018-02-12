# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from wdb import set_trace as depurador


class Repair(models.Model):
    _name = 'car_workshop.repair'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    # track_visibility=True Si quiero hacer seguimiendo de quien hace los cambios
    # incluirlo en los campos que se quiere el seguimiento

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle', store=True)

    sale_order_id = fields.Many2one('sale.order', delegate=True, required=True, ondelete='restrict')
    project_task_id = fields.Many2one('project.task', required=True, ondelete='restrict')
    stage_id = fields.Many2one(group_expand='_read_group_stage_ids', related="project_task_id.stage_id", store=True)
    description = fields.Html(related="project_task_id.description", store=True)
    project_id = fields.Many2one(related="project_task_id.project_id", store=True)
    user_id = fields.Many2one(related="project_task_id.user_id", store=True)
    kanban_state = fields.Selection(related="project_task_id.kanban_state", default='normal', store=True)
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
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_project_id' in self.env.context:
            search_domain = ['|', ('project_ids', '=', self.env.context['default_project_id'])] + search_domain
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

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

        print(vals)
        # IMPORTANTE: las sale.order DEBEN tener un nombre único y calculado?
        # O pueden tener un nombre descriptivo. O usar un campo, "descripción"
        rec = super(Repair, self).create(vals)
        return rec

    @api.multi
    def unlink(self):
        # Solo se pueden borrar task y sale asociados si primero se borra el repair con el que están asociados.
        for repair in self:
            if repair.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete a sent quotation or a sales order! Try to cancel it before.'))
        task_records = self.env["project.task"].search([('id', '=', self.project_task_id.id)])
        sale_records = self.env["sale.order"].search([('id', '=', self.sale_order_id.id)])
        super(Repair, self).unlink()
        for record in task_records:
            record.unlink()
        for record in sale_records:
            record.unlink()
        return True

    @api.multi
    def action_quotation_send(self):
        return self.sale_order_id.action_quotation_send()

    @api.multi
    def action_confirm(self):
        return self.sale_order_id.action_confirm()

    @api.multi
    def print_quotation(self):
        return self.sale_order_id.print_quotation()

    @api.multi
    def action_cancel(self):
        return self.sale_order_id.action_cancel()

    @api.multi
    def action_draft(self):
        return self.sale_order_id.action_draft()

    @api.multi
    def action_done(self):
        return self.sale_order_id.action_done()

    @api.multi
    def action_unlock(self):
        self.sale_order_id.action_unlock()

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'user_id': self.partner_id.user_id.id or self.env.uid
        }
        if self.env['ir.config_parameter'].sudo().get_param(
                'sale.use_sale_note') and self.env.user.company_id.sale_note:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note

        if self.partner_id.team_id:
            values['team_id'] = self.partner_id.team_id.id
        self.update(values)

    @api.onchange('project_id')
    def _onchange_project(self):
        if self.project_id:
            if self.project_id not in self.stage_id.project_ids:
                self.stage_id = self.project_task_id.stage_find(self.project_id.id, [('fold', '=', False)])
        else:
            self.stage_id = False


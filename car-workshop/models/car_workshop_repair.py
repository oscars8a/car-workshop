# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from wdb import set_trace as depurador


class Repair(models.Model):
    _name = 'car_workshop.repair'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    # track_visibility=True Si quiero hacer seguimiendo de quien hace los cambios
    # incluirlo en los campos que se quiere el seguimiento

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=True, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle', store=True, )
    repair_title = fields.Char()

    sale_order_id = fields.Many2one('sale.order', delegate=True, required=True, ondelete='restrict')
    repair_line = fields.One2many('sale.order.line', 'repair_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)

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
    priority = fields.Selection(related="project_task_id.priority")

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_project_id' in self.env.context:
            search_domain = ['|', ('project_ids', '=', self.env.context['default_project_id'])] + search_domain
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['repair_title'] = str(vals['name'])
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'sale.order') or _('')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('')

        rec_task = self.project_task_id.create(vals).id
        vals['project_task_id'] = rec_task
        if 'message_follower_ids' in vals:
            vals.pop('message_follower_ids')
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
    def _action_confirm(self):
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'confirmation_date': fields.Datetime.now()
        })
        
        if self.env.context.get('send_email'):
            self.force_quotation_send()

        # create an analytic account if at least an expense product
        if any([expense_policy != 'no' for expense_policy in self.order_line.mapped('product_id.expense_policy')]):
            if not self.analytic_account_id:
                self._create_analytic_account()
        return self.sale_order_id._action_confirm()

    @api.multi
    def action_confirm(self):
        auto_done = self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting')
        for sale in self:
            for order in sale.sale_order_id:
                order.state = 'sale'
            if auto_done:
                sale.sale_order_id.action_done()
        return self.sale_order_id.action_confirm()

    @api.multi
    def print_quotation(self):
        return self.sale_order_id.print_quotation()

    @api.multi
    def action_quotation_send(self):
        return self.sale_order_id.action_quotation_send()

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
    def action_view_invoice(self):
        return self.sale_order_id.action_view_invoice()

    @api.multi
    def action_view_delivery(self):
        return self.sale_order_id.action_view_delivery()

    @api.multi
    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if self.vehicle_id and self.vehicle_id.customer_id:
            self.partner_id = self.vehicle_id.customer_id
                
        
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
            'pricelist_id': self.partner_id.property_product_pricelist
                            and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id
                               and self.partner_id.property_payment_term_id.id or False,
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

    @api.multi
    @api.onchange('partner_shipping_id', 'partner_id')
    def onchange_partner_shipping_id(self):
        """
        Trigger the change of fiscal position when the shipping address is modified.
        """
        self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id,
                                                                                          self.partner_shipping_id.id)
        return {}

    @api.onchange('fiscal_position_id')
    def _compute_tax_id(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed on the SO.
        """
        for order in self:
            order.order_line._compute_tax_id()

    @api.onchange('project_id')
    def _onchange_project(self):
        if self.project_id:
            if self.project_id not in self.stage_id.project_ids:
                self.stage_id = self.project_task_id.stage_find(self.project_id.id, [('fold', '=', False)])
        else:
            self.stage_id = False

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        order_ids = [record.sale_order_id.id for record in self]
        sale_obj = self.env['sale.order'].browse(order_ids)
        invoice_id = (sale_obj.action_invoice_create(grouped=False, final=False))
        return invoice_id

    # Para generar la Hoja de Admision. Falta.
    @api.multi
    def admission_sheet(self):
        # return self.env.ref('car_worshop.admission_sheet_report').admission_sheet(self)
        pass
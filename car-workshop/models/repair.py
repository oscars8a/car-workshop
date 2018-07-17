# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
#from wdb import set_trace as depurador


class Repair(models.Model):
    _name = 'car_workshop.repair'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'id desc'


    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=True, )
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle', store=True, )
    name = fields.Char(default="",required=True)
    repair_title = fields.Char()
    finished_stage = fields.Boolean("Finished")
    material_line_ids = fields.One2many(comodel_name="car_workshop.material_line", inverse_name="repair_id",
                                    string="Material Lines", auto_join=True)


    sale_order_id = fields.Many2one('sale.order', delegate=True, required=True, ondelete='restrict')
    repair_line = fields.One2many(comodel_name='sale.order.line', inverse_name='repair_id', string='Order Lines',
                                  states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                  copy=True)

    budget_resignation = fields.Boolean(string="Budged Resignation")
    collect_pieces = fields.Boolean(string="Collect Pieces")


    project_task_id = fields.Many2one('project.task', required=True, ondelete='restrict')
    stage_id = fields.Many2one(group_expand='_read_group_stage_ids', related="project_task_id.stage_id", store=True)
    description = fields.Text(string="Descripción")
    project_id = fields.Many2one(related="project_task_id.project_id", store=True, required=True)
    user_id = fields.Many2one(related="project_task_id.user_id", store=True)
    kanban_state = fields.Selection(related="project_task_id.kanban_state", default='normal', store=True)
    date_start = fields.Datetime(related="project_task_id.date_start", string="Entry Date", store=True)
    date_deadline = fields.Datetime(string="Deadline Date")
    tag_ids = fields.Many2many(related="project_task_id.tag_ids")
    timesheet_ids = fields.One2many(related="project_task_id.timesheet_ids")
    planned_hours = fields.Float(related="project_task_id.planned_hours")
    total_hours_spent = fields.Float(related="project_task_id.total_hours_spent")
    progress = fields.Float(related="project_task_id.progress")
    effective_hours = fields.Float(related="project_task_id.effective_hours")
    children_hours = fields.Float(related="project_task_id.children_hours")
    remaining_hours = fields.Float(related="project_task_id.remaining_hours")
    priority = fields.Selection(related="project_task_id.priority")

    color = fields.Integer('Color Index', compute="change_colore_on_kanban")


    purchase_count = fields.Integer(compute="_compute_purchase_count")
    purchase_ids = fields.Many2many(comodel_name='purchase.order',relation="repair_purchase")

    @api.model
    def _compute_purchase_count(self):
        for record in self:
            record.purchase_count = len(self.purchase_ids.ids)

    @api.depends('finished_stage')
    def change_colore_on_kanban(self):
        for record in self:
            color = 0
            if record.finished_stage:
                color = 1 #Rojo
            record.color = color

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
            new_name = self.env['ir.sequence'].search([('code','=','sale.order')])[0]
            digit = int(new_name.number_next_actual)
            if digit < 10:
                vals['name'] = "SO00"+str(new_name.number_next_actual)
            elif digit < 100:
                vals['name'] = "SO0" + str(new_name.number_next_actual)
            else:
                vals['name'] = "SO" + str(new_name.number_next_actual)
        if not vals.get('date_start'):
            vals['date_start'] = fields.Date.context_today(self)
        rec_task = self.project_task_id.create(vals).id
        vals['project_task_id'] = rec_task
        if 'message_follower_ids' in vals:
            vals.pop('message_follower_ids')
        rec = super(Repair, self).create(vals)

        #Meto el id de la orden de reparación en el
        rec.sale_order_id.write({'repair_id':rec.id})

        # Metemos lineas de Presupuesto en Materiales
        order_line_ids = rec.order_line
        warehouse = self.env['stock.warehouse'].search([], limit=1)
        location_id = warehouse.lot_stock_id.id
        location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
        for line in order_line_ids:
            if line.product_id.type != "service":
                vars = {
                    'product_uom': line.product_uom.id,
                    'product_uom_qty': line.product_uom_qty,
                    'consumed': False,
                    'to_quotation': True,
                    'repair_id': rec.id,
                    'location_id': location_id,
                    'location_dest_id': location_dest_id,
                    'product_id': line.product_id.id,
                    'name': line.name
                }
                self.env['car_workshop.material_line'].create(vars)
        return rec

    @api.multi
    def write(self, vals):
        # Metemos lineas de Presupuesto en Materiales

        if 'order_line' in vals and vals['order_line']:
            warehouse = self.env['stock.warehouse'].search([], limit=1)
            location_id = warehouse.lot_stock_id.id
            location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
            lines_vars = vals['order_line']
            for lines in lines_vars:
                if lines[2]:
                    mt_line = lines[2]
                    if 'product_id' in mt_line.keys() and mt_line['product_id']:
                        product_obj = self.env['product.product'].browse([mt_line['product_id']])
                        if product_obj.type != 'service':
                            vars = {
                                'product_uom': mt_line["product_uom"],
                                'product_uom_qty': mt_line["product_uom_qty"],
                                'consumed': False,
                                'to_quotation': True,
                                'repair_id': self.id,
                                'location_id': location_id,
                                'location_dest_id': location_dest_id,
                                'product_id': mt_line["product_id"],
                                'name': mt_line["name"]
                            }
                            self.env['car_workshop.material_line'].create(vars)
        super(Repair, self).write(vals)


    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.repair_title))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.repair_title)
        else:
            new_name = u"Copy of {} ({})".format(self.repair_title, copied_count)
        default['name'] = new_name
        rec = super(Repair, self).copy(default)
        rec.user_id = None
        return rec

    @api.multi
    def unlink(self):
        # Solo se pueden borrar task y sale asociados si primero se borra el repair con el que están asociados.
        for repair in self:
            if repair.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete a sent quotation or a sales order! Try to cancel it before.'))
            task_records = self.env["project.task"].search([('id', '=', repair.project_task_id.id)])
            sale_records = self.env["sale.order"].search([('id', '=', repair.sale_order_id.id)])
            super(Repair, repair).unlink()
            for record in task_records:
                record.unlink()
            for record in sale_records:
                record.unlink()
        return True

    @api.multi
    def action_confirm(self):

        auto_done = self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting')
        for repair in self:
            for order in repair.sale_order_id:
                order.state = 'sale'
            if auto_done:
                repair.sale_order_id.action_done()
        return self.sale_order_id.action_confirm()

    @api.multi
    def print_quotation(self):
        return self.env.ref('car-workshop.action_report_quotation').report_action(self, data=None)

    @api.multi
    def action_cw_quotation_send(self):
        '''
                This function opens a window to compose an email, with the carworshop repair quotation
                template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            # Hay que definir una plantilla para mostrar en el mensaje.
            # Hay que hacer una plantilla asociada a la anterior para definir
            template_id = ir_model_data.get_object_reference('car-workshop', 'email_template_cw_quotationn')[1]
        except ValueError:
            template_id = False
        try:
            # Que narices es esto?
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'car_workshop.repair',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_template_data_notification_email_sale_order",
            'force_email': True,
            'force_website': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

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
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            if self.vehicle_id.customer_id:
                self.partner_id = self.vehicle_id.customer_id

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
        }
        if self.env['ir.config_parameter'].sudo().get_param(
                'sale.use_sale_note') and self.env.user.company_id.sale_note:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note
        if self.partner_id.team_id:
            values['team_id'] = self.partner_id.team_id.id
        self.update(values)

        vehicles_list = self.env['fleet.vehicle'].search([('customer_id.id', '=', self.partner_id.id)])
        vehicles_count = len(vehicles_list)
        if vehicles_count == 1:
            self.vehicle_id = vehicles_list[0]
        elif vehicles_count > 1:
            if self.vehicle_id and self.vehicle_id.customer_id.id != self.partner_id.id:
                self.vehicle_id = False


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
        print(self.id)
        if self.project_id:
            if self.project_id not in self.stage_id.project_ids:
                self.stage_id = self.project_task_id.stage_find(self.project_id.id, [('fold', '=', False)])
        else:
            self.stage_id = False

    @api.multi
    def action_admission_sheet(self):
        return self.env.ref('car-workshop.action_report_admission_sheet').report_action(self, data=None)

    @api.multi
    def action_finised(self):
        self.finished_stage = not self.finished_stage

    @api.multi
    def action_purchases(self):
        # action_view_invoice en purchase.order
        domain = "[('id', 'in', " + str(self.purchase_ids.ids) + "),]"
        # domain = "[]"
        return {
            "name": _("Purchases"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_id": "form",
            "view_mode": "form",
            "view_type": "form",
            "views": [[False, "tree"], [False, "form"], [False, "search"]],
            "domain": domain,
            "target": "current",
        }
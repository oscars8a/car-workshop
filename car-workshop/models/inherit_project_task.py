# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, float_round
from odoo.osv import osv
from datetime import date

class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids

    @api.depends('product_line_ids.price_total')
    def _amount_all(self):
        for order in self:
            amount_tax = 0.0
            for line in order.product_line_ids:
                amount_tax += line.price_total
            order.update({
                'amount_total': amount_tax,
            })

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    product_line_ids = fields.One2many('project.task.product.line', 'product_line_id', string='ProductLines', copy=True, auto_join=True)
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',required=True, readonly=True,default=_default_warehouse_id)
    state = fields.Selection([
        ('waiting', 'Ready'),
        ('workshop_create_invoices', 'Invoiced'),
        ('cancel', 'Invoice Canceled'),
    ], string='Status', readonly=True, default='waiting', track_visibility='onchange', select=True)
    image_client_vehicle = fields.Binary(related='vehicle_id.image_client_vehicle')

    @api.multi
    def workshop_create_invoices(self):

        self.state = 'workshop_create_invoices'
        inv_obj = self.env['account.invoice']
        inv_line_obj = self.env['account.invoice.line']
        customer = self.vehicle_id.driver_id
        if not customer.name:
            raise osv.except_osv(_('UserError!'), _('Please select a Customer.'))

        company_id = self.env['res.users'].browse(1).company_id
        currency_value = company_id.currency_id.id
        self.ensure_one()
        journal_id = 1
        inv_data = {
            'name': customer.name,
            'reference': customer.name,
            'account_id': customer.property_account_receivable_id.id,
            'partner_id': customer.id,
            'currency_id': currency_value,
            'journal_id': journal_id,
            'origin': self.name,
            'company_id': company_id.id,
        }
        inv_id = inv_obj.create(inv_data)
        for records in self.product_line_ids:
            if records.product_id.id:
                income_account = records.product_id.property_account_income_id.id
            if not income_account:
                income_account=1
            inv_line_data = {
                'name': records.product_id.name,
                'account_id': income_account,
                'price_unit': records.price_unit,
                'quantity': records.product_uom_qty,
                'product_id': records.product_id.id,
                'invoice_id': inv_id.id,
                'tax_ids': records.product_id.taxes_id,
            }
            inv_line_obj.create(inv_line_data)

        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')

        result = {
            'name': action.name,
            'help': action.help,
            'type': 'ir.actions.act_window',
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'],
                      [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': 'account.invoice',
        }
        if len(inv_id) > 1:
            result['domain'] = "[('id','in',%s)]" % inv_id.ids
        elif len(inv_id) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = inv_id.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        invoiced_records = self.env['project.task']

        total = 0
        for rows in invoiced_records:
            invoiced_date = rows.date
            invoiced_date = invoiced_date[0:10]
            if invoiced_date == str(date.today()):
                total = total + rows.price_subtotal
        return result


class ProductLine(models.Model):
    _name = 'project.task.product.line'
    _description = 'Product Lines'

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_total': line.product_uom_qty*line.price_unit,
            })

    product_id = fields.Many2one('product.template', string='Products', required=True)
    product_uom_qty = fields.Integer(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    product_line_id = fields.Many2one('project.task', string="Task Reference", required=True, ondelete='cascade', index=True, copy=False)
    price_total = fields.Float(compute='_compute_amount', string='Total Amount', store=True)

    @api.onchange('product_id')
    def get_price(self):
        self.price_unit = self.product_id.lst_price

    @api.onchange('product_uom_qty', 'product_id')
    def _onchange_product_id_check_availability(self):
        if not self.product_id or not self.product_uom_qty:
            return {}
        if self.product_id.type == 'product':
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            product = self.product_id.with_context(warehouse=self.product_line_id.warehouse_id.id)
            product_qty = self._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
            if float_compare(product.virtual_available, product_qty, precision_digits=precision) == -1:
                is_available = False
                if not is_available:
                    message = _('You plan to sell %s %s but you only have %s %s available in %s warehouse.') % \
                              (self.product_uom_qty, self.product_id.name, product.virtual_available,
                               product.uom_id.name, self.product_line_id.warehouse_id.name)
                    warning_mess = {
                        'title': _('Not enough inventory!'),
                        'message': message
                    }
                    return {'warning': warning_mess}
        return {}

    @api.multi
    def _compute_quantity(self, qty, to_unit, round=True, rounding_method='UP'):
        if not self:
            return qty
        self.ensure_one()
        #amount = qty / self.factor
        amount = qty
        if to_unit:
            amount = amount * to_unit.factor
            if round:
                amount = float_round(amount, precision_rounding=to_unit.rounding, rounding_method=rounding_method)
        return amount

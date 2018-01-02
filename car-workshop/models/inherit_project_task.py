# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, float_round

class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids

    @api.depends('material_line_ids.price_total')
    def _amount_all(self):
        for order in self:
            amount_tax = 0.0
            for line in order.material_line_ids:
                amount_tax += line.price_total
            order.update({
                'amount_total': amount_tax,
            })

    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )
    material_line_ids = fields.One2many('project.task.material.line', 'material_line_id', string='Material Lines')
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all')
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=True,
        default=_default_warehouse_id)

class MaterialLine(models.Model):
    _name = 'project.task.material.line'
    _description = 'Material Lines'

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_total': line.product_uom_qty*line.price_unit,
            })

    product_id = fields.Many2one('product.template', string='Products')
    product_uom_qty = fields.Integer(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    material_line_id = fields.Many2one('project.task', string="Task Reference", ondelete='cascade')
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
            product = self.product_id.with_context(warehouse=self.material_line_id.warehouse_id.id)
            product_qty = self._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
            if float_compare(product.virtual_available, product_qty, precision_digits=precision) == -1:
                is_available = False
                if not is_available:
                    message = _('You plan to sell %s %s but you only have %s %s available in %s warehouse.') % \
                              (self.product_uom_qty, self.product_id.name, product.virtual_available,
                               product.uom_id.name, self.material_line_id.warehouse_id.name)
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

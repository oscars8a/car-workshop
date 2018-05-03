# -*- coding: utf-8 -*-

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from wdb import set_trace as depurador


class CarSaleAdvancePaymentInv(models.TransientModel):
    _name = 'car_workshop.advance.payment.inv'
    _inherit = 'sale.advance.payment.inv'

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        """
        Este método sirve para para meter el campo descripción de la orden de reparación asociado en la factura.
        Solo funciona para los cobros en porcentaje o un monto fijo.
        :param order:
        :param so_line:
        :param amount:
        :return:
        """
        invoice = super(CarSaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        repair_obj = self.env["car_workshop.repair"].search([('sale_order_id','=',order.id)])[0]
        invoice.description = repair_obj.description
        return invoice

    @api.multi
    def create_invoices_for_carworkshop(self):
        repair_objs = self.env['car_workshop.repair'].browse(self._context.get('active_ids',[]))
        active_sales = []
        for repair in repair_objs:
            active_sales.append(repair.sale_order_id.id)
        sale_orders = self.env['sale.order'].browse(active_sales)
        if self.advance_payment_method == 'delivered':
            sale_orders.action_invoice_create()
        elif self.advance_payment_method == 'all':
            sale_orders.action_invoice_create(final=True)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                if self.advance_payment_method == 'percentage':
                    amount = order.amount_untaxed * self.amount / 100
                else:
                    amount = self.amount
                if self.product_id.invoice_policy != 'order':
                    raise UserError(_(
                        'The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_(
                        "The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(
                    lambda r: not order.company_id or r.company_id == order.company_id)
                if order.fiscal_position_id and taxes:
                    tax_ids = order.fiscal_position_id.map_tax(taxes).ids
                else:
                    tax_ids = taxes.ids
                context = {'lang': order.partner_id.lang}
                so_line = sale_line_obj.create({
                    'name': _('Advance: %s') % (time.strftime('%m %Y'),),
                    'price_unit': amount,
                    'product_uom_qty': 0.0,
                    'order_id': order.id,
                    'discount': 0.0,
                    'product_uom': self.product_id.uom_id.id,
                    'product_id': self.product_id.id,
                    'tax_id': [(6, 0, tax_ids)],
                    'is_downpayment': True,
                })
                del context
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}
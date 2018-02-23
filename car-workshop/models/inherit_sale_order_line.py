from odoo import api, fields, models,_

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    repair_id = fields.Many2one('car_workshop.repair')

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        if 'pricelist_id' in self._context and 'partner_id' in self._context:
            partner = self.env['res.partner'].browse(self._context['partner_id'])
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=partner.id,
                quantity=vals.get('product_uom_qty') or self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self._context['pricelist_id'],
                uom=self.product_uom.id
            )
            vals['price_unit'] = product.price
        self.update(vals)

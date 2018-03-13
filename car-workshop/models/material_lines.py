# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from wdb import set_trace as depurador


class StockMove(models.Model):
    _inherit = 'stock.move'

    car_work_repair_id = fields.Many2one('car_workshop.repair')


class MaterialLine(models.Model):
    _name = "car_workshop.material_line"

    repair_id = fields.Many2one('car_workshop.repair', string='Car Workshop Order Repair', required=True,
                                ondelete='cascade', index=True, copy=False)

    location_id = fields.Many2one('stock.location', 'Source Location', index=True, required=True)
    location_dest_id = fields.Many2one('stock.location', 'Dest. Location', index=True, required=True)
    move_id = fields.Many2one('stock.move', 'Inventory Move', copy=False, readonly=True)

    product_id = fields.Many2one('product.product', 'Product', required=True)
    name = fields.Text(string='Description', required=True)

    product_uom_qty = fields.Float('Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'),
                                   required=True)
    product_uom = fields.Many2one('product.uom', 'Product Unit of Measure', required=True)

    @api.onchange('repair_id')
    def onchange_operation_repair_id(self):

        self.onchange_product_id()
        args = self.repair_id.company_id and [('company_id', '=', self.repair_id.company_id.id)] or []
        warehouse = self.env['stock.warehouse'].search(args, limit=1)
        self.location_id = warehouse.lot_stock_id
        self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id

    @api.multi
    def consume_done(self):
        pass


    # Obtener la descripción de product_id
    @api.onchange('repair_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        """ On change of product it sets product quantity, tax account, name,
        uom of product, unit price and price subtotal. """
        partner = self.repair_id.partner_id
        pricelist = self.repair_id.pricelist_id
        if not self.product_id or not self.product_uom_qty:
            return
        if self.product_id:
            if partner:
                self.name = self.product_id.with_context(lang=partner.lang).display_name
            else:
                self.name = self.product_id.display_name
            self.product_uom = self.product_id.uom_id.id
        if self.type != 'remove':
            if partner and self.product_id:
                self.tax_id = partner.property_account_position_id.map_tax(self.product_id.taxes_id, self.product_id,
                                                                           partner).ids
            warning = False
            if not pricelist:
                warning = {
                    'title': _('No Pricelist!'),
                    'message':
                        _(
                            'You have to select a pricelist in the Repair form !\n Please set one before choosing a product.')}
            else:
                price = pricelist.get_product_price(self.product_id, self.product_uom_qty, partner)
                if price is False:
                    warning = {
                        'title': _('No valid pricelist line found !'),
                        'message':
                            _(
                                "Couldn't find a pricelist line matching this product and quantity.\nYou have to change either the product, the quantity or the pricelist.")}
                else:
                    self.price_unit = price
            if warning:
                return {'warning': warning}
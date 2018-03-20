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

    repair_id = fields.Many2one(comodel_name="car_workshop.repair", string="repair_id", required=True, ondelete="cascade",
                               index=True, copy=False)


    location_id = fields.Many2one('stock.location', 'Source Location', index=True, required=True)
    location_dest_id = fields.Many2one('stock.location', 'Dest. Location', index=True, required=True)
    move_id = fields.Many2one('stock.move', 'Inventory Move', copy=False, readonly=True)

    product_id = fields.Many2one('product.product', 'Product', required=True)
    name = fields.Text(string='Description', required=True)

    product_uom_qty = fields.Float('Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'),
                                   required=True)
    product_uom = fields.Many2one('product.uom', 'Product Unit of Measure', required=True)

    # @api.onchange('repair_id')
    # def onchange_operation_repair_id(self):
    #
    #     # self.onchange_product_id()


    @api.multi
    def consume_done(self):
        # depurador()
        pass


    # Obtener la descripción de product_id
    @api.onchange('repair_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        partner = self.repair_id.partner_id
        if not self.product_id or not self.product_uom_qty:
            return
        if self.product_id:
            if partner:
                self.name = self.product_id.with_context(lang=partner.lang).display_name
            else:
                self.name = self.product_id.display_name
            self.product_uom = self.product_id.uom_id.id

        args = self.repair_id.company_id and [('company_id', '=', self.repair_id.company_id.id)] or []
        warehouse = self.env['stock.warehouse'].search(args, limit=1)
        self.location_id = warehouse.lot_stock_id
        self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
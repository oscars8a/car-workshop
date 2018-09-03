from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    repair_ids = fields.Many2many(comodel_name='car_workshop.repair', relation="repair_purchase")

    @api.model
    def create(self, vals):
        if 'repair_id' in self._context.keys():
            vals['repair_ids'] = [(4,self._context['repair_id'],_)]
        rec = super(PurchaseOrder, self).create(vals)
        return rec

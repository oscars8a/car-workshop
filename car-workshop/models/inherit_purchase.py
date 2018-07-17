from odoo import api, fields, models, _
from wdb import set_trace as depurador


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    repair_ids = fields.Many2many(comodel_name='car_workshop.repair', relation="repair_purchase")

    @api.model
    def create(self, vals):
        print(vals)
        print(self._context)
        rec = super(PurchaseOrder, self).create(vals)
        depurador()
        # Registro el repair_id en el campo repair_ids
        if self._context['active_model'] == 'car_workshop.repair':
            values = {self._context['active_id'],rec.id}
            rec.write({
                'repair_ids':[(4,self._context['active_id'],_)]
            })
        return rec

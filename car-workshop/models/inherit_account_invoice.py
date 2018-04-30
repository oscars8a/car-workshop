from odoo import api, fields, models
from wdb import set_trace as depurador

class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    def _compu_aux_descrip(self):
        return self.description != ''

    description = fields.Html(string="Description")
    aux_descrip = fields.Boolean(string="", compute=_compu_aux_descrip)

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        sale_id = self.env['sale.order'].search([('name','=',vals['origin'])])[0].id
        obj = self.env['car_workshop.repair'].search([('sale_order_id',"=",sale_id)])[0]
        vals['description'] = obj.description
        return vals
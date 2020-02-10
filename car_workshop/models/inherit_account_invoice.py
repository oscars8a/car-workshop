from odoo import api, fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    description = fields.Html(string="Description")
    vehicle_id = fields.Many2one(comodel_name="fleet.vehicle", string="Vehicle", required=False, )

    def workshop_invoice_print(self):
        self.ensure_one()
        self.sent = True
        return self.env.ref('car_workshop.cw_action_report_invoice').report_action(self)

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        """
        Este método sirve para para meter el campo descripción de la orden de reparación asociado en la factura.
        Solo funciona para los cobros de lineas.
        *** Y el campo vehículo.
        :return:
        """
        vals = super(SaleOrder, self)._prepare_invoice()
        sale_ids = self.env['sale.order'].search([('name','=',vals['origin'])])
        if len(sale_ids) == 1:
            sale_id = sale_ids[0].id
            car_objs = self.env['car_workshop.repair'].search([('sale_order_id',"=",sale_id)])
            if len(car_objs) ==1:
                vals['description'] = car_objs[0].description
                vals['vehicle_id'] = car_objs[0].vehicle_id.id
        return vals

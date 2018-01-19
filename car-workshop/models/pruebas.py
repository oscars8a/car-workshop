from odoo import api, fields, models, _


class Pruebas(models.Model):
    _inherit = 'project.task'


    @api.model
    def create(self, vals):
        print('HI ODOO DEVELOPER')
        print(vals)
        rec = super(Pruebas, self).create(vals)
        print('REGISTRO')
        print(rec)
        return rec

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from wdb import set_trace as depurador

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_mylang(self, cr, uid, context=None):
        ids = self.pool.get('res.lang').search(cr, uid, [], context=context)
        res = self.pool.get('res.lang').read(cr, uid, ids, ['code', 'name'], context)
        return [(j['code'], j['name']) for j in res] + [('', '')]

    _defaults = {
        'lang':_get_mylang,
    }
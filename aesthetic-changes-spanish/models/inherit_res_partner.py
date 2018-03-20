# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.model
    def _lang_get(self):

        return self.env['res.lang'].get_installed()

    languages = []
    languages = _lang_get
    # if "es_ES" in tuplas for languages:


    lang = fields.Selection(_lang_get, string='Language', default=lambda self: self.env.lang,
                            help="If the selected language is loaded in the system, all documents related to "
                                 "this contact will be printed in this language. If not, it will be English.")
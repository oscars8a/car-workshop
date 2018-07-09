# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TireWizard(models.TransientModel):
    _name = 'tire_catalog.tire_wizard'

    widthSelection = []
    for x in range(145, 255, 10):
        widthSelection.append((str(x), str(x)))
    widthSelection.append((str(140), str(140)))
    widthSelection.append((str(150), str(150)))
    heightSelection = []
    for x in range(40, 80, 5):
        heightSelection.append((str(x), str(x)))

    diameterSelection = []
    for x in range(13, 18):
        diameterSelection.append((str(x), str(x)))

    width = fields.Selection(string="Width", selection=widthSelection, required=False, )
    height = fields.Selection(string="Height", selection=heightSelection, required=False, )
    diameter = fields.Selection(string="Diameter", selection=diameterSelection, required=False, )
    brand_id = fields.Many2one(comodel_name="tire_catalog.tire_brand", string="Brand", required=False, )
    season = fields.Selection(string="Season",
                              selection=[('summer', 'Summer'), ('winter', 'Winter'), ('allseason', 'All season')],
                              required=False, )

    @api.multi
    def create_request(self):
        domain = [("is_a_tire","=",True)]
        context = {}
        if self.width:
            context["search_default_width"] = self.width
        if self.height:
            context["search_default_height"] = self.height
        if self.diameter:
            context["search_default_diameter"] = self.diameter
        if self.brand_id:
            context["search_default_brand_id"] = self.brand_id.id
        if self.season:
            context["search_default_season"] = self.season
        return {
            "name": _("Tires"),
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "views": [[False,"kanban"],[False, "form"],[False, "tree"],[False, "search"]],
            "context": context,
            "domain": domain,
            "target": "main",
        }


# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TireWizard(models.TransientModel):
    _name = 'tire_catalog.tire_wizard'

    widthSelection = []
    for x in range(145, 255, 10):
        widthSelection.append((str(x), str(x)))

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

        # Probar a ponerlo como contexto para que el usuario pueda cambiarlo
        domain = [("is_a_tire","=",True)]
        context = {}
        if self.width:
            # domain.append(("width","=",str(self.width)))
            context["search_default_width"] = self.width
        if self.height:
            # domain.append(("height","=",str(self.height)))
            context["search_default_height"] = self.height
        if self.diameter:
            # domain.append(("diameter","=",str(self.diameter)))
            context["search_default_diameter"] = self.diameter
        if self.brand_id:
            # domain.append(("brand_id","=",str(self.brand_id.name)))
            context["search_default_brand_id"] = self.brand_id.id
        if self.season is not False:
            # domain.append(("season","=",str(self.season)))
            context["search_default_season"] = self.season

        # search_id = self.env.ref("car-workshop.car-workshop_fleet_wheels_view_search")

        return {

            "name": "Tires",
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "views": [[False,"kanban"],[False, "form"],[False, "search"]],
            "context": context,
            "domain": domain,
            # Modificarlo cuando este solucionado el problema de los filtros.
            # Tener el nombre de la vista search como referencia.
            # "search_view_id": (search_id.id, "car-workshop.fleet.wheels.view.search"),
            "target": "main",
        }


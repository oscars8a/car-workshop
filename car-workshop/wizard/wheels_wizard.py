# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class WheelsWizard(models.TransientModel):
    _name = 'car_workshop.wheels_wizard'

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
    brand_id = fields.Many2one(comodel_name="car_workshop.wheels_brands", string="Brand", required=False, )
    season = fields.Selection(string="Season",
                              selection=[('summer', 'Summer'), ('winter', 'Winter'), ('allseason', 'All season')],
                              required=False, )

    @api.multi
    def create_request(self):
        print("You click finish")
        domain = [("is_wheel","=",True)]
        if self.width:
            domain.append(("width","=",str(self.width)))

        if self.height:
            domain.append(("height","=",str(self.height)))

        if self.diameter:
            domain.append(("diameter","=",str(self.diameter)))

        if self.brand_id:

            domain.append(("brand_id","=",str(self.brand_id.name)))

        if self.season is not False:
            domain.append(("season","=",str(self.season)))

        print(domain)

        return {
            "name": "Wheels",
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "views": [[False,"kanban"],[False, "form"]],
            "domain": domain,
            "target": "main",
        }
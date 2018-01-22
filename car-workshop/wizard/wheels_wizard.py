# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class WheelsWizard(models.TransientModel):
    _name = 'car_workshop.wheels_wizard'


    widthSelection = []
    for x in range(145,255,10):
        widthSelection.append((str(x),str(x)))
    width = fields.Selection(string="Width", selection=widthSelection, required=False, )

    heightSelection = []
    for x in range(40,80,5):
        heightSelection.append((str(x),str(x)))
    height = fields.Selection(string="Height", selection=heightSelection, required=False, )

    diameterSelection = []
    for x in range(13, 18):
        diameterSelection.append((str(x), str(x)))
    diameter = fields.Selection(string="Diameter", selection=diameterSelection, required=False, )



    brandsSelection = [('orium', 'ORIUM'), ('firestone', 'FireStone'), ('feuvert', 'FeuVert'), ('michelin', 'MICHELIN'),
                       ('continental', 'CONTINENTAL')]
    brands = fields.Selection(string="Brands", selection=brandsSelection, required=False, )
    season = fields.Selection(string="Season",
                              selection=[('summer', 'Summer'), ('winter', 'Winter'), ('allseason', 'All season')],
                              required=False, )

    @api.multi
    def create_request(self):
        print("You click finish")
        
        return True

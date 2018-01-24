from odoo import api, fields, models,_

class WheelsBrands(models.Model):
    _name = 'car_workshop.wheels_brands'
    _inherit = 'fleet.vehicle.model.brand'

from odoo import api, fields, models,_

class Wheels(models.Model):

    _inherit = 'product.product'

    is_wheel = fields.Boolean(string="It's a wheel?",  )

    widthSelection = []
    for x in range(145, 255, 10):
        widthSelection.append((str(x), str(x)))
    width = fields.Selection(string="Width", selection=widthSelection, required=False, )

    heightSelection = []
    for x in range(40, 80, 5):
        heightSelection.append((str(x), str(x)))
    height = fields.Selection(string="Height", selection=heightSelection, required=False, )

    diameterSelection = []
    for x in range(13, 18):
        diameterSelection.append((str(x), str(x)))
    diameter = fields.Selection(string="Diameter", selection=diameterSelection, required=False, )

    brand_id = fields.Many2one(comodel_name="car_workshop.wheels_brands", string="Brand", required=False, )
    season = fields.Selection(string="Season",
                              selection=[('summer', 'Summer'), ('winter', 'Winter'), ('allseason', 'All season')],
                              required=False, )


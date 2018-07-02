from odoo import api, fields, models,_

class Tire(models.Model):

    _inherit = 'product.template'

    is_a_tire = fields.Boolean(string="It's a tire?",  )

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


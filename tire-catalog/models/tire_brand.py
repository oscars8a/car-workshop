from odoo import api, fields, models, tools, _


class TireBrand(models.Model):
    _name = 'tire_catalog.tire_brand'

    name = fields.Char('Make', required=True)
    image = fields.Binary("Logo", attachment=True,
                          help="This field holds the image used as logo for the brand, limited to 1024x1024px.")
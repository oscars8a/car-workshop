from odoo import api, fields, models, tools, _


class TireBrand(models.Model):
    _name = 'tire_catalog.tire_brand'

    name = fields.Char('Make', required=True)
    image = fields.Binary("Logo", attachment=True,
                          help="This field holds the image used as logo for the brand, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized image", attachment=True,
                                 help="Medium-sized logo of the brand. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
                                help="Small-sized logo of the brand. It is automatically "
                                     "resized as a 64x64px image, with aspect ratio preserved. "
                                     "Use this field anywhere a small image is required.")

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(TireBrand, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(TireBrand, self).write(vals)
# -*- coding: utf-8 -*-
{
    'name': 'SDI Tire Catalog',
    'version': '11.0.1.0.0',
    'summary': "Catalog for Tires",
    'description': 'Complete catalog for tires.',
    'category': 'Industries',
    'author':
        'Óscar Soto, '
        'SDI Soluciones Informáticas',
    'website': 'https://github.com/oscars8a/car-workshop.git',
    'license': 'AGPL-3',
    'depends': [
        'car-workshop',
    ],
    'data': [
        'wizards/tire_wizard_view.xml',
        'views/inherit_product_template.xml',
        'views/inherit_product_product.xml',
        'views/tire_brand.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/tire_branches.xml',
    ],
    'installable': True,
}

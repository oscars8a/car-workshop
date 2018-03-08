# -*- coding: utf-8 -*-
{
    'name': 'SDI Car Workshop',
    'version': '11.0.1.0.0',
    'summary': "Complete Vehicle Workshop Operations & Reports.",
    'description': 'Vehicle workshop operations & Its reports',
    'category': 'Industries',
    'author':
        'Óscar Soto, '
        'SDI Soluciones Informáticas',
    'website': 'https://github.com/oscars8a/car-workshop.git',
    'license': 'AGPL-3',
    'depends': [
        'project',
        'fleet',
        'hr_timesheet',
        'account_invoicing',
        'product',
        'stock',
        'sale_stock',
        'sale_management',
    ],
    'data': [
        'views/car-workshop.xml',
        'wizards/inherit_sale_make_invoice_advance_views.xml',
        'views/repair.xml',
        'views/inherit_project_project.xml',
        'views/inherit_fleet_vehicle.xml',
        'data/branches.xml',
        'data/models.xml',
        'data/project_initial.xml',
        'views/inherit_res_partner.xml',
        'views/inherit_res_config_settings.xml',
    ],
    'demo': [
    ],
    'installable': True,
}

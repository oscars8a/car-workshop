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
        'html_text'
    ],
    'data': [
        'views/car-workshop.xml',
        'wizards/inherit_sale_make_invoice_advance_views.xml',
        'report/cw_assets.xml',
        'report/cw_head_templates.xml',
        'report/cw_admission_sheet_templates.xml',
        'report/cw_invoice_templates.xml',
        'report/cw_quotation_templates.xml',
        'report/cw_reports.xml',
        'views/repair.xml',
        'views/inherit_project_project.xml',
        'views/inherit_fleet_vehicle.xml',
        'data/branches.xml',
        'data/models.xml',
        'data/project_initial.xml',
        'views/inherit_res_partner.xml',
        'views/inherit_res_config_settings.xml',
        'security/car-workshop_security.xml',
        'security/ir.model.access.csv',
        'views/inherit_account_invoice.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'post_init_hook':'main',
}

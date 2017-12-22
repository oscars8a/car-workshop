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
    'license': 'GPL-3',
    'depends': [
        'project',
        'fleet',
        'hr_timesheet',
        'account_invoicing',
    ],
    'data': [
        'views/car-workshop.xml',
        'views/inherit_fleet_vehicle.xml',
        'views/inherit_project_project.xml',
        'views/inherit_project_task.xml',
    ],
    'installable': True,
}

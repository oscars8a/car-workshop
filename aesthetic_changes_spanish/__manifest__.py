# -*- coding: utf-8 -*-
{
    'name': 'SDI Aesthetic Changes Fleet for Spanish version',
    'version': '11.0.1.0.0',
    'summary': "Changes in the module Fleet to SDI.",
    'description': 'Changes in the module Fleet for SDI. Change the order in fleet model form view, '
                   'first Make second Model name.',
    'category': 'Industries',
    'author':
        'Óscar Soto, '
        'SDI Soluciones Informáticas',
    'website': 'https://github.com/oscars8a/car-workshop.git',
    'license': 'AGPL-3',
    'depends': [
        'fleet',
    ],
    'data': [
        'views/inherit_fleet_vehicle_model.xml',
    ],
    'installable': True,
}

# -*- coding: utf-8 -*-
{
    'name': 'SDI Separate Project and CarWorkshop',
    'version': '11.0.1.0.0',
    'summary': "Separate Project and CarWorkshop",
    'description': 'Changes in the module Fleet for SDI. Change the order in fleet model form view, '
                   'first Make second Model name.',
    'category': '',
    'author':
        'Óscar Soto, '
        'SDI Soluciones Informáticas',
    'website': 'https://github.com/SDIsl/car-workshop.git',
    'license': 'AGPL-3',
    'depends': [
        'car_workshop',
    ],
    'data': [
        'views/inherit_project_project.xml'
    ],
    'installable': True,
}

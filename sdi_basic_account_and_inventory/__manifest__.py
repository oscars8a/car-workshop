{
    'name': 'SDi Contabilidad e Inventario Básico ',
    'version': '11.0.1.0.0',
    'summary': '...',
    'description': '...',
    'category': '...',
    'author':
        'Óscar Soto, '
        'SDI Soluciones Informáticas',
    'website': 'https://github.com/oscars8a/car-workshop.git',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'sale_management',
        'account_invoicing',
        'stock',
        'l10n_es_vat_book',
        'car-workshop',
    ],
    'data': [
        'views/basic_account.xml',
        'views/basic_sales.xml',
        'views/basic_purchases.xml',
    ],
    'installable': True,
    'auto_install': False,
}
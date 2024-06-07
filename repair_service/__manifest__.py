{
    'name': 'Repair Service ',
    'version': '17.0',
    'license': 'LGPL-3',
    'category': 'Repair',
    'sequence': -500,
    'summary': 'Manage repair services and link them to repair orders and sales orders',
    'depends': ['repair', 'sale'],
    'data': ['security\ir.model.access.csv',
             'views\service.xml',
             'views/repair_order_view.xml'
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

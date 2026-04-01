{
    'name': 'Car Rental',
    'version': '19.0.1.0.0',
    'summary': 'Manage car rental operations',
    'description': """
Car Rental Module
=================
This module allows you to manage your car rental business:
- Manage your fleet of rental cars
- Create and track rental orders
- Monitor car availability
- Compute rental costs automatically
    """,
    'category': 'Services/Rental',
    'author': 'Odoo Community',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/car_views.xml',
        'views/rental_order_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

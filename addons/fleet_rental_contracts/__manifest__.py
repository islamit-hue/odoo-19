# -*- coding: utf-8 -*-
{
    'name': 'Fleet Rental Contracts',
    'version': '19.0.1.0.0',
    'category': 'Fleet',
    'summary': 'Manage car rental contracts with checklists, damages and sketches',
    'description': """
        Fleet Rental Contracts addon for Odoo 19.
        Features:
        - Rental contracts with sequence RENT/YEAR/NNNNN
        - Branch management (single company branches)
        - Checkout/checkin checklists prefilled from last vehicle contract
        - Damage tracking
        - SVG + PNG sketches for vehicle condition
        - PDF report
    """,
    'author': 'islamit-hue',
    'depends': ['base', 'fleet', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/rental_plan.xml',
        'views/rental_branch_views.xml',
        'views/rental_contract_views.xml',
        'report/rental_contract_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'fleet_rental_contracts/static/src/js/sketch_widget.js',
            'fleet_rental_contracts/static/src/xml/sketch_widget.xml',
            'fleet_rental_contracts/static/src/scss/sketch_widget.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
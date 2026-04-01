# -*- coding: utf-8 -*-
from odoo import fields, models


class RentalDamage(models.Model):
    _name = 'fleet.rental.damage'
    _description = 'Rental Damage'
    _order = 'date desc, id'

    contract_id = fields.Many2one(
        'fleet.rental.contract',
        string='Contract',
        ondelete='cascade',
        required=True,
    )
    date = fields.Date(string='Date', default=fields.Date.today)
    description = fields.Char(string='Description', required=True)
    location = fields.Char(string='Location on Vehicle')
    severity = fields.Selection(
        [
            ('minor', 'Minor'),
            ('moderate', 'Moderate'),
            ('major', 'Major'),
        ],
        string='Severity',
        default='minor',
    )
    repair_cost = fields.Float(string='Estimated Repair Cost')
    notes = fields.Text(string='Notes')

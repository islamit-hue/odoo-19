# -*- coding: utf-8 -*-
from odoo import fields, models


class RentalChecklistLine(models.Model):
    _name = 'fleet.rental.checklist.line'
    _description = 'Rental Checklist Line'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    contract_id = fields.Many2one(
        'fleet.rental.contract',
        string='Contract',
        ondelete='cascade',
    )
    checklist_type = fields.Selection(
        [('checkout', 'Checkout'), ('checkin', 'Checkin')],
        string='Type',
        required=True,
        default='checkout',
    )
    name = fields.Char(string='Item', required=True)
    condition = fields.Selection(
        [
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('poor', 'Poor'),
            ('damaged', 'Damaged'),
        ],
        string='Condition',
        default='good',
    )
    notes = fields.Text(string='Notes')

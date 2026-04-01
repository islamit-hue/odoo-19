# -*- coding: utf-8 -*-
from odoo import fields, models


class RentalBranch(models.Model):
    _name = 'rental.branch'
    _description = 'Rental Branch'
    _order = 'name'

    name = fields.Char(string='Branch Name', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
        required=True,
    )
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    active = fields.Boolean(default=True)

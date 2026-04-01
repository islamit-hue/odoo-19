from odoo import fields, models


class FleetRentalBranch(models.Model):
    _name = "fleet.rental.branch"
    _description = "Rental Branch"

    name = fields.Char(string="Branch Name", required=True)
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    phone = fields.Char(string="Phone")
    manager_id = fields.Many2one("res.users", string="Branch Manager")
    active = fields.Boolean(default=True)

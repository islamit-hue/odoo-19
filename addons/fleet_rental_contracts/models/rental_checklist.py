from odoo import fields, models


class RentalChecklistItem(models.Model):
    _name = "rental.checklist.item"
    _description = "Rental Vehicle Checklist Item"
    _rec_name = "name"

    name = fields.Char(string="Item Name", required=True)
    category = fields.Selection(
        [
            ("exterior", "Exterior"),
            ("interior", "Interior"),
            ("mechanical", "Mechanical"),
            ("documents", "Documents"),
            ("accessories", "Accessories"),
        ],
        string="Category",
        default="exterior",
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class RentalContractChecklist(models.Model):
    _name = "rental.contract.checklist"
    _description = "Contract Checklist Entry"

    contract_id = fields.Many2one(
        "rental.contract",
        string="Contract",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        "rental.checklist.item", string="Checklist Item", required=True
    )
    checklist_type = fields.Selection(
        [("checkout", "Check-Out"), ("checkin", "Check-In")],
        string="Type",
        required=True,
        default="checkout",
    )
    condition = fields.Selection(
        [("ok", "OK"), ("damaged", "Damaged"), ("missing", "Missing")],
        string="Condition",
        default="ok",
    )
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Photo", attachment=True)


class RentalViolation(models.Model):
    _name = "rental.violation"
    _description = "Traffic / Parking Violation"
    _rec_name = "name"

    name = fields.Char(string="Violation Reference", required=True)
    contract_id = fields.Many2one("rental.contract", string="Contract")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    partner_id = fields.Many2one("res.partner", string="Customer")
    violation_type = fields.Selection(
        [
            ("traffic", "Traffic Violation"),
            ("parking", "Parking Violation"),
            ("damage", "Damage / Misuse"),
        ],
        string="Violation Type",
        default="traffic",
    )
    violation_date = fields.Date(string="Violation Date")
    amount = fields.Float(string="Amount")
    description = fields.Text(string="Description")
    state = fields.Selection(
        [("pending", "Pending"), ("charged", "Charged"), ("waived", "Waived")],
        string="Status",
        default="pending",
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
    )

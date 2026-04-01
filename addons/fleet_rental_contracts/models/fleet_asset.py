from odoo import fields, models


class FleetVehicleInherit(models.Model):
    """Extend fleet.vehicle with rental-specific fields."""

    _inherit = "fleet.vehicle"

    branch_id = fields.Many2one("rental.branch", string="Assigned Branch")
    vehicle_status = fields.Selection(
        [
            ("available", "Available"),
            ("rented", "Rented"),
            ("maintenance", "Under Maintenance"),
            ("accident", "Accident"),
            ("total_loss", "Total Loss"),
            ("service", "Service"),
            ("substitute", "Substitute"),
            ("traffic_hold", "Traffic Hold"),
            ("stolen", "Stolen"),
            ("transferred", "In Transfer"),
        ],
        string="Vehicle Status",
        default="available",
    )
    insurance_company = fields.Char(string="Insurance Company")
    insurance_policy_number = fields.Char(string="Insurance Policy Number")
    insurance_type = fields.Selection(
        [
            ("comprehensive", "Comprehensive"),
            ("third_party", "Third Party"),
        ],
        string="Insurance Type",
    )
    insurance_expiry_date = fields.Date(string="Insurance Expiry Date")
    fuel_type = fields.Selection(
        [
            ("gasoline", "Gasoline"),
            ("diesel", "Diesel"),
            ("hybrid", "Hybrid"),
            ("electric", "Electric"),
        ],
        string="Fuel Type",
    )
    rental_contract_ids = fields.One2many(
        "rental.contract", "vehicle_id", string="Rental Contracts"
    )
    rental_contract_count = fields.Integer(
        compute="_compute_rental_contract_count", string="# Rental Contracts"
    )

    def _compute_rental_contract_count(self):
        for rec in self:
            rec.rental_contract_count = len(rec.rental_contract_ids)

    def action_view_rental_contracts(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Rental Contracts",
            "res_model": "rental.contract",
            "view_mode": "list,form",
            "domain": [("vehicle_id", "=", self.id)],
            "context": {"default_vehicle_id": self.id},
        }

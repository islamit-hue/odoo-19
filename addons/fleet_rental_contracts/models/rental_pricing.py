from odoo import fields, models


class RentalPricing(models.Model):
    _name = "rental.pricing"
    _description = "Rental Pricing Plan"
    _rec_name = "name"

    name = fields.Char(string="Pricing Plan Name", required=True)
    branch_id = fields.Many2one("rental.branch", string="Branch")
    vehicle_category = fields.Char(string="Vehicle Category")
    vehicle_model = fields.Char(string="Vehicle Model")
    manufacture_year = fields.Integer(string="Manufacture Year")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Specific Vehicle")
    partner_id = fields.Many2one("res.partner", string="Specific Customer")

    period_type = fields.Selection(
        [
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("hourly", "Hourly"),
            ("sub_3", "3-Month Subscription"),
            ("sub_6", "6-Month Subscription"),
            ("sub_9", "9-Month Subscription"),
            ("sub_12", "12-Month Subscription"),
            ("sub_24", "24-Month Subscription"),
            ("sub_36", "36-Month Subscription"),
        ],
        string="Period Type",
        required=True,
        default="daily",
    )

    price = fields.Float(string="Base Price", required=True)
    allowed_km = fields.Float(string="Allowed KM")
    allowed_hours = fields.Float(string="Allowed Hours")
    extra_km_price = fields.Float(string="Extra KM Price")
    extra_hour_price = fields.Float(string="Extra Hour Price")
    open_km_price = fields.Float(string="Open KM Price (per day)")
    insurance_comprehensive_price = fields.Float(
        string="Comprehensive Insurance Price"
    )
    insurance_comprehensive_no_deductible = fields.Float(
        string="Comprehensive Insurance (No Deductible)"
    )
    delivery_price = fields.Float(string="Delivery Price")
    extra_driver_price = fields.Float(string="Extra Driver Price")
    deductible_amount = fields.Float(string="Deductible Amount")
    active = fields.Boolean(default=True)
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        string="Currency",
    )
    notes = fields.Text(string="Notes")

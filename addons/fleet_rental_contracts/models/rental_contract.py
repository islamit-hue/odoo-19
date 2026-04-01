import math

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FleetRentalChecklist(models.Model):
    _name = "fleet.rental.checklist"
    _description = "Rental Contract Checklist"

    contract_id = fields.Many2one(
        "fleet.rental.contract", string="Contract", required=True, ondelete="cascade"
    )
    name = fields.Char(string="Item", required=True)
    checklist_type = fields.Selection(
        [("checkout", "Checkout"), ("checkin", "Checkin")],
        string="Type",
        required=True,
        default="checkout",
    )
    checked = fields.Boolean(string="Checked", default=False)
    notes = fields.Char(string="Notes")


class FleetRentalDamage(models.Model):
    _name = "fleet.rental.damage"
    _description = "Rental Contract Damage"

    contract_id = fields.Many2one(
        "fleet.rental.contract", string="Contract", required=True, ondelete="cascade"
    )
    name = fields.Char(string="Description", required=True)
    location = fields.Char(string="Location on Vehicle")
    damage_type = fields.Selection(
        [
            ("scratch", "Scratch"),
            ("dent", "Dent"),
            ("crack", "Crack"),
            ("missing", "Missing Part"),
            ("other", "Other"),
        ],
        string="Damage Type",
        default="scratch",
    )
    date = fields.Date(string="Date", default=fields.Date.context_today)
    photo = fields.Binary(string="Photo")
    photo_filename = fields.Char(string="Photo Filename")


class FleetRentalContract(models.Model):
    _name = "fleet.rental.contract"
    _description = "Fleet Rental Contract"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "date_start desc, id desc"

    name = fields.Char(
        string="Contract Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        tracking=True,
    )
    driver_name = fields.Char(string="Driver Name")
    driver_license = fields.Char(string="Driver License No.")
    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        string="Vehicle",
        required=True,
        tracking=True,
    )
    branch_id = fields.Many2one(
        "fleet.rental.branch",
        string="Rental Branch",
        tracking=True,
    )
    date_start = fields.Datetime(
        string="Rental Start",
        required=True,
        default=fields.Datetime.now,
        tracking=True,
    )
    date_end = fields.Datetime(
        string="Rental End",
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    daily_rate = fields.Monetary(
        string="Daily Rate",
        currency_field="currency_id",
    )
    rental_days = fields.Integer(
        string="Rental Days",
        compute="_compute_rental_days",
        store=True,
    )
    total_amount = fields.Monetary(
        string="Total Amount",
        compute="_compute_total_amount",
        store=True,
        currency_field="currency_id",
    )
    checklist_ids = fields.One2many(
        "fleet.rental.checklist",
        "contract_id",
        string="Checkout Checklist",
        domain=[("checklist_type", "=", "checkout")],
    )
    checkin_checklist_ids = fields.One2many(
        "fleet.rental.checklist",
        "contract_id",
        string="Checkin Checklist",
        domain=[("checklist_type", "=", "checkin")],
    )
    damage_ids = fields.One2many(
        "fleet.rental.damage",
        "contract_id",
        string="Damages",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("ongoing", "Ongoing"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        tracking=True,
        copy=False,
    )
    notes = fields.Text(string="Notes")

    @api.depends("date_start", "date_end")
    def _compute_rental_days(self):
        for record in self:
            if record.date_start and record.date_end:
                delta = record.date_end - record.date_start
                record.rental_days = max(1, math.ceil(delta.total_seconds() / 86400))
            else:
                record.rental_days = 0

    @api.depends("rental_days", "daily_rate")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.rental_days * record.daily_rate

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "fleet.rental.contract"
                ) or _("New")
        return super().create(vals_list)

    @api.constrains("date_start", "date_end")
    def _check_dates(self):
        for record in self:
            if record.date_end < record.date_start:
                raise ValidationError(_("Rental end date must be after start date."))

    def action_confirm(self):
        self.write({"state": "confirmed"})

    def action_start(self):
        self.write({"state": "ongoing"})

    def action_done(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_reset_draft(self):
        self.write({"state": "draft"})

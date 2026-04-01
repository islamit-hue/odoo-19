from odoo import api, fields, models


class RentalContract(models.Model):
    _name = "rental.contract"
    _description = "Car Rental Contract"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Contract Number",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("suspended", "Suspended"),
            ("legal", "Sent to Legal"),
            ("insurance", "Sent to Insurance"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    # Customer
    partner_id = fields.Many2one(
        "res.partner", string="Customer", required=True, tracking=True
    )
    partner_type = fields.Selection(
        [
            ("individual", "Individual"),
            ("company", "Company"),
            ("government", "Government Entity"),
        ],
        string="Customer Type",
        default="individual",
    )
    customer_source = fields.Selection(
        [
            ("thaqib_app", "Thaqib App"),
            ("talqani_app", "Talqani App"),
            ("karwa_app", "Karwa App"),
            ("online_other", "Other Online"),
            ("branch_direct", "Direct from Branch"),
        ],
        string="Customer Source",
    )

    # Branch & Vehicle
    branch_id = fields.Many2one("rental.branch", string="Branch", tracking=True)
    close_branch_id = fields.Many2one(
        "rental.branch",
        string="Closing Branch",
        help="Branch where the vehicle is returned if different from opening branch.",
    )
    inter_branch_delivery_fee = fields.Float(string="Inter-Branch Delivery Fee")
    vehicle_id = fields.Many2one(
        "fleet.vehicle", string="Vehicle", required=True, tracking=True
    )
    pricing_id = fields.Many2one("rental.pricing", string="Pricing Plan")

    # Dates
    start_date = fields.Datetime(
        string="Start Date / Time", required=True, tracking=True
    )
    end_date = fields.Datetime(
        string="Expected End Date / Time", required=True, tracking=True
    )
    actual_return_date = fields.Datetime(
        string="Actual Return Date / Time", tracking=True
    )

    # Mileage
    km_start = fields.Float(string="Odometer at Start (km)")
    km_end = fields.Float(string="Odometer at Return (km)")
    km_driven = fields.Float(
        string="KM Driven", compute="_compute_km_driven", store=True
    )
    allowed_km = fields.Float(string="Allowed KM")
    extra_km = fields.Float(
        string="Extra KM", compute="_compute_extra_km", store=True
    )
    extra_km_charge = fields.Float(
        string="Extra KM Charge", compute="_compute_extra_km", store=True
    )

    # Additional drivers
    additional_driver_ids = fields.Many2many(
        "res.partner", string="Additional Drivers"
    )
    extra_driver_charge = fields.Float(string="Extra Driver Charge")

    # Financial
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
    )
    base_amount = fields.Float(string="Base Rental Amount")
    deposit_amount = fields.Float(string="Security Deposit")
    advance_payment = fields.Float(string="Advance Payment")
    insurance_charge = fields.Float(string="Insurance Charge")
    delivery_charge = fields.Float(string="Delivery Charge")
    deductible_charge = fields.Float(string="Deductible Charge")
    open_km_charge = fields.Float(string="Open KM Charge")
    total_amount = fields.Float(
        string="Total Amount", compute="_compute_total_amount", store=True
    )
    amount_paid = fields.Float(string="Amount Paid")
    amount_due = fields.Float(
        string="Amount Due", compute="_compute_amount_due", store=True
    )

    # Grace period for cancellation (minutes)
    grace_minutes = fields.Integer(
        string="Grace Period (minutes)",
        default=60,
        help="Time allowed to close/cancel the contract without charges.",
    )

    # Checklists & violations
    checkout_checklist_ids = fields.One2many(
        "rental.contract.checklist",
        "contract_id",
        domain=[("checklist_type", "=", "checkout")],
        string="Check-Out Checklist",
    )
    checkin_checklist_ids = fields.One2many(
        "rental.contract.checklist",
        "contract_id",
        domain=[("checklist_type", "=", "checkin")],
        string="Check-In Checklist",
    )
    violation_ids = fields.One2many(
        "rental.violation", "contract_id", string="Violations"
    )
    violation_count = fields.Integer(
        compute="_compute_violation_count", string="# Violations"
    )

    # Insurance
    insurance_type = fields.Selection(
        [
            ("none", "None"),
            ("comprehensive", "Comprehensive"),
            ("comprehensive_no_deductible", "Comprehensive (No Deductible)"),
            ("third_party", "Third Party"),
        ],
        string="Insurance Type",
        default="none",
    )

    notes = fields.Text(string="Internal Notes")
    invoice_ids = fields.Many2many("account.move", string="Invoices")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "rental.contract"
                ) or "New"
        return super().create(vals_list)

    @api.depends("km_start", "km_end")
    def _compute_km_driven(self):
        for rec in self:
            rec.km_driven = max(0.0, (rec.km_end or 0.0) - (rec.km_start or 0.0))

    @api.depends("km_driven", "allowed_km", "pricing_id")
    def _compute_extra_km(self):
        for rec in self:
            extra = max(0.0, rec.km_driven - rec.allowed_km)
            rec.extra_km = extra
            price = rec.pricing_id.extra_km_price if rec.pricing_id else 0.0
            rec.extra_km_charge = extra * price

    @api.depends(
        "base_amount",
        "insurance_charge",
        "delivery_charge",
        "deductible_charge",
        "open_km_charge",
        "extra_km_charge",
        "extra_driver_charge",
        "inter_branch_delivery_fee",
    )
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = (
                rec.base_amount
                + rec.insurance_charge
                + rec.delivery_charge
                + rec.deductible_charge
                + rec.open_km_charge
                + rec.extra_km_charge
                + rec.extra_driver_charge
                + rec.inter_branch_delivery_fee
            )

    @api.depends("total_amount", "amount_paid", "deposit_amount", "advance_payment")
    def _compute_amount_due(self):
        for rec in self:
            rec.amount_due = (
                rec.total_amount - rec.amount_paid - rec.advance_payment
            )

    @api.depends("violation_ids")
    def _compute_violation_count(self):
        for rec in self:
            rec.violation_count = len(rec.violation_ids)

    # ---------- Actions ----------

    def action_open(self):
        self.write({"state": "open"})

    def action_suspend(self):
        self.write({"state": "suspended"})

    def action_close(self):
        self.write({"state": "closed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_send_to_legal(self):
        self.write({"state": "legal"})

    def action_send_to_insurance(self):
        self.write({"state": "insurance"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})

    def action_view_violations(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Violations",
            "res_model": "rental.violation",
            "view_mode": "list,form",
            "domain": [("contract_id", "=", self.id)],
            "context": {"default_contract_id": self.id},
        }

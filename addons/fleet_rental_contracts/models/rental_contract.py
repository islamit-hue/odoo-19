# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FleetRentalContract(models.Model):
    _name = 'fleet.rental.contract'
    _description = 'Fleet Rental Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Contract Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('active', 'Active'),
            ('returned', 'Returned'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
        required=True,
    )
    branch_id = fields.Many2one('rental.branch', string='Branch')
    partner_id = fields.Many2one(
        'res.partner', string='Customer', required=True, tracking=True
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle', string='Vehicle', required=True, tracking=True
    )
    license_plate = fields.Char(
        related='vehicle_id.license_plate', string='License Plate', store=True
    )
    date_start = fields.Date(
        string='Checkout Date', required=True, default=fields.Date.today
    )
    date_end = fields.Date(string='Expected Return Date')
    date_return = fields.Date(string='Actual Return Date')

    # Rental plan / pricing
    rental_plan_id = fields.Many2one('fleet.rental.plan', string='Rental Plan')
    daily_rate = fields.Float(string='Daily Rate', digits=(10, 2))
    duration_days = fields.Integer(string='Duration (Days)', compute='_compute_duration', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total', store=True, digits=(10, 2))

    # Odometer
    odometer_out = fields.Float(string='Odometer Out (km)')
    odometer_in = fields.Float(string='Odometer In (km)')

    # Checklists
    checkout_line_ids = fields.One2many(
        'fleet.rental.checklist.line',
        'contract_id',
        string='Checkout Checklist',
        domain=[('checklist_type', '=', 'checkout')],
    )
    checkin_line_ids = fields.One2many(
        'fleet.rental.checklist.line',
        'contract_id',
        string='Checkin Checklist',
        domain=[('checklist_type', '=', 'checkin')],
    )

    # Damages
    damage_ids = fields.One2many(
        'fleet.rental.damage', 'contract_id', string='Damages'
    )

    # Sketches (SVG + PNG stored as Text/Binary)
    sketch_out_svg = fields.Text(string='Sketch Out (SVG)')
    sketch_out_image = fields.Image(string='Sketch Out (PNG)', max_width=1024, max_height=1024)
    sketch_in_svg = fields.Text(string='Sketch In (SVG)')
    sketch_in_image = fields.Image(string='Sketch In (PNG)', max_width=1024, max_height=1024)

    notes = fields.Text(string='Notes')

    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                rec.duration_days = (rec.date_end - rec.date_start).days
            else:
                rec.duration_days = 0

    @api.depends('duration_days', 'daily_rate')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = rec.duration_days * rec.daily_rate

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('fleet.rental.contract') or 'New'
        return super().create(vals_list)

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if not self.vehicle_id:
            return
        self._prefill_checklists()

    def _prefill_checklists(self):
        """Prefill checkout/checkin lines from the last contract for same vehicle."""
        if not self.vehicle_id:
            return
        last_contract = self.search(
            [('vehicle_id', '=', self.vehicle_id.id), ('id', '!=', self._origin.id or 0)],
            order='date_start desc, id desc',
            limit=1,
        )
        checkout_lines = []
        checkin_lines = []
        if last_contract:
            for line in last_contract.checkout_line_ids:
                checkout_lines.append((0, 0, {
                    'name': line.name,
                    'sequence': line.sequence,
                    'checklist_type': 'checkout',
                    'condition': 'good',
                }))
            for line in last_contract.checkin_line_ids:
                checkin_lines.append((0, 0, {
                    'name': line.name,
                    'sequence': line.sequence,
                    'checklist_type': 'checkin',
                    'condition': 'good',
                }))
        else:
            # Default checklist items
            default_items = [
                'Exterior Body',
                'Windows & Mirrors',
                'Tires & Wheels',
                'Fuel Level',
                'Engine Oil',
                'Interior Cleanliness',
                'Air Conditioning',
                'Headlights & Signals',
                'Spare Tire & Tools',
                'Documents in Vehicle',
            ]
            for i, item in enumerate(default_items):
                checkout_lines.append((0, 0, {
                    'name': item,
                    'sequence': (i + 1) * 10,
                    'checklist_type': 'checkout',
                    'condition': 'good',
                }))
                checkin_lines.append((0, 0, {
                    'name': item,
                    'sequence': (i + 1) * 10,
                    'checklist_type': 'checkin',
                    'condition': 'good',
                }))
        self.checkout_line_ids = checkout_lines
        self.checkin_line_ids = checkin_lines

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_activate(self):
        self.write({'state': 'active'})

    def action_return(self):
        self.write({'state': 'returned', 'date_return': fields.Date.today()})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})


class FleetRentalPlan(models.Model):
    _name = 'fleet.rental.plan'
    _description = 'Fleet Rental Plan'
    _order = 'name'

    name = fields.Char(string='Plan Name', required=True)
    plan_type = fields.Selection(
        [('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        string='Type',
        default='daily',
        required=True,
    )
    rate = fields.Float(string='Rate', digits=(10, 2), required=True)
    active = fields.Boolean(default=True)

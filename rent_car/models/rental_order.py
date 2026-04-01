from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class RentCarOrder(models.Model):
    _name = 'rent.car.order'
    _description = 'Car Rental Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
        tracking=True,
    )
    car_id = fields.Many2one(
        'rent.car',
        string='Car',
        required=True,
        tracking=True,
        domain=[('state', '!=', 'maintenance')],
    )
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True,
    )
    date_from = fields.Date(
        string='Rental Start',
        required=True,
        tracking=True,
    )
    date_to = fields.Date(
        string='Rental End',
        required=True,
        tracking=True,
    )
    duration = fields.Integer(
        string='Duration (Days)',
        compute='_compute_duration',
        store=True,
    )
    daily_rate = fields.Float(
        string='Daily Rate',
        digits=(10, 2),
        related='car_id.daily_rate',
        store=True,
        readonly=True,
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
        digits=(10, 2),
        tracking=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='car_id.currency_id',
        store=True,
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('ongoing', 'Ongoing'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        copy=False,
    )
    notes = fields.Text(
        string='Notes',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.depends('date_from', 'date_to')
    def _compute_duration(self):
        for order in self:
            if order.date_from and order.date_to:
                delta = order.date_to - order.date_from
                order.duration = max(delta.days, 1)
            else:
                order.duration = 0

    @api.depends('duration', 'daily_rate')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = order.duration * order.daily_rate

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('rent.car.order') or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        for order in self:
            if order.state != 'draft':
                raise UserError(_('Only draft orders can be confirmed.'))
            self._check_car_availability(order)
            order.write({'state': 'confirmed'})

    def action_start(self):
        for order in self:
            if order.state != 'confirmed':
                raise UserError(_('Only confirmed orders can be started.'))
            order.car_id.write({'state': 'rented'})
            order.write({'state': 'ongoing'})

    def action_done(self):
        for order in self:
            if order.state != 'ongoing':
                raise UserError(_('Only ongoing rentals can be marked as done.'))
            order.car_id.write({'state': 'available'})
            order.write({'state': 'done'})

    def action_cancel(self):
        for order in self:
            if order.state in ('done',):
                raise UserError(_('Done orders cannot be cancelled.'))
            if order.state == 'ongoing':
                order.car_id.write({'state': 'available'})
            order.write({'state': 'cancelled'})

    def action_reset_draft(self):
        for order in self:
            if order.state != 'cancelled':
                raise UserError(_('Only cancelled orders can be reset to draft.'))
            order.write({'state': 'draft'})

    def _check_car_availability(self, order):
        overlapping = self.search([
            ('car_id', '=', order.car_id.id),
            ('id', '!=', order.id),
            ('state', 'in', ('confirmed', 'ongoing')),
            ('date_from', '<=', order.date_to),
            ('date_to', '>=', order.date_from),
        ])
        if overlapping:
            raise ValidationError(
                _('Car "%s" is already booked for the selected period.') % order.car_id.name
            )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for order in self:
            if order.date_from and order.date_to:
                if order.date_to < order.date_from:
                    raise ValidationError(_('Rental end date must be after the start date.'))

    @api.onchange('car_id')
    def _onchange_car_id(self):
        if self.car_id:
            self.daily_rate = self.car_id.daily_rate

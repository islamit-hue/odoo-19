from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RentCar(models.Model):
    _name = 'rent.car'
    _description = 'Rental Car'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Car Name',
        required=True,
        tracking=True,
    )
    brand = fields.Char(
        string='Brand',
        required=True,
        tracking=True,
    )
    model = fields.Char(
        string='Model',
        required=True,
        tracking=True,
    )
    year = fields.Integer(
        string='Year',
        tracking=True,
    )
    color = fields.Char(
        string='Color',
        tracking=True,
    )
    plate_number = fields.Char(
        string='Plate Number',
        required=True,
        tracking=True,
        copy=False,
    )
    daily_rate = fields.Float(
        string='Daily Rate',
        required=True,
        digits=(10, 2),
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('rented', 'Rented'),
            ('maintenance', 'Under Maintenance'),
        ],
        string='Status',
        default='available',
        required=True,
        tracking=True,
    )
    image = fields.Image(
        string='Car Image',
        max_width=1920,
        max_height=1920,
    )
    image_128 = fields.Image(
        string='Car Image 128',
        related='image',
        max_width=128,
        max_height=128,
        store=True,
    )
    description = fields.Text(
        string='Description',
    )
    order_count = fields.Integer(
        string='Rental Orders',
        compute='_compute_order_count',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )

    def _compute_order_count(self):
        RentalOrder = self.env['rent.car.order']
        for car in self:
            car.order_count = RentalOrder.search_count([('car_id', '=', car.id)])

    def action_set_available(self):
        self.write({'state': 'available'})

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})

    def action_view_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Rental Orders'),
            'res_model': 'rent.car.order',
            'view_mode': 'list,form',
            'domain': [('car_id', '=', self.id)],
            'context': {'default_car_id': self.id},
        }

    @api.constrains('plate_number')
    def _check_plate_number(self):
        for car in self:
            if car.plate_number:
                duplicate = self.search([
                    ('plate_number', '=', car.plate_number),
                    ('id', '!=', car.id),
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        _('Plate number "%s" is already used by another car.') % car.plate_number
                    )

    @api.constrains('daily_rate')
    def _check_daily_rate(self):
        for car in self:
            if car.daily_rate <= 0:
                raise ValidationError(_('Daily rate must be greater than zero.'))

    @api.constrains('year')
    def _check_year(self):
        for car in self:
            if car.year and (car.year < 1900 or car.year > 2100):
                raise ValidationError(_('Please enter a valid year (1900–2100).'))

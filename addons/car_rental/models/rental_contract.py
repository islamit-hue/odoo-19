from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RentalContract(models.Model):
    _name = 'rental.contract'
    _description = 'عقد تأجير سيارة'

    name = fields.Char(string='رقم العقد', readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='العميل', required=True)
    car_id = fields.Many2one('rental.car', string='السيارة', required=True)
    date_from = fields.Date(string='تاريخ الاستلام', required=True)
    date_to = fields.Date(string='تاريخ التسليم', required=True)
    total_days = fields.Integer(
        string='عدد الأيام', compute='_compute_days', store=True)
    total_amount = fields.Float(
        string='المبلغ الإجمالي', compute='_compute_amount', store=True)
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('confirmed', 'مؤكد'),
        ('active', 'جارٍ'),
        ('done', 'منتهي'),
        ('cancelled', 'ملغي'),
    ], default='draft', string='الحالة')
    note = fields.Text(string='ملاحظات')

    @api.depends('date_from', 'date_to')
    def _compute_days(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                rec.total_days = (rec.date_to - rec.date_from).days
            else:
                rec.total_days = 0

    @api.depends('total_days', 'car_id.daily_rate')
    def _compute_amount(self):
        for rec in self:
            rec.total_amount = rec.total_days * rec.car_id.daily_rate

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('rental.contract')
                    or 'New'
                )
        return super().create(vals_list)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise ValidationError(
                    'تاريخ الاستلام يجب أن يكون قبل تاريخ التسليم!'
                )

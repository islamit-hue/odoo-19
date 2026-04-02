from odoo import models, fields


class RentalCar(models.Model):
    _name = 'rental.car'
    _description = 'سيارة للتأجير'

    name = fields.Char(string='اسم السيارة', required=True)
    license_plate = fields.Char(string='رقم اللوحة', required=True)
    brand = fields.Char(string='الماركة')
    model_year = fields.Integer(string='سنة الصنع')
    daily_rate = fields.Float(string='السعر اليومي')
    state = fields.Selection([
        ('available', 'متاحة'),
        ('rented', 'مؤجرة'),
        ('maintenance', 'في الصيانة'),
    ], string='الحالة', default='available')
    image = fields.Binary(string='صورة السيارة', attachment=True)

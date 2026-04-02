# Car Rental (car_rental)

وحدة Odoo 19 لإدارة تأجير السيارات بشكل متكامل.

## الميزات

- **إدارة السيارات**: تسجيل بيانات كل سيارة (الاسم، اللوحة، الماركة، السنة، السعر اليومي، الحالة).
- **عقود التأجير**: إنشاء وإدارة عقود التأجير مع حساب تلقائي لعدد الأيام والمبلغ الإجمالي.
- **ترقيم تلقائي**: كل عقد يحصل على رقم تسلسلي تلقائي بصيغة `RC/YYYY/XXXX`.
- **طباعة العقود**: تقرير PDF جاهز للطباعة لكل عقد تأجير.
- **التحقق من البيانات**: التحقق من صحة تواريخ الاستلام والتسليم.

## الاعتماديات

| الوحدة   | السبب                              |
|----------|------------------------------------|
| `base`   | النماذج الأساسية في Odoo           |
| `sale`   | إدارة المبيعات والفواتير           |
| `fleet`  | نماذج المركبات الجاهزة             |
| `account`| المحاسبة والمدفوعات                |

## نماذج البيانات

### `rental.car` — السيارة
| الحقل         | النوع     | الوصف                |
|---------------|-----------|----------------------|
| name          | Char      | اسم السيارة          |
| license_plate | Char      | رقم اللوحة           |
| brand         | Char      | الماركة              |
| model_year    | Integer   | سنة الصنع            |
| daily_rate    | Float     | السعر اليومي         |
| state         | Selection | available/rented/maintenance |
| image         | Binary    | صورة السيارة         |

### `rental.contract` — عقد التأجير
| الحقل        | النوع     | الوصف                          |
|--------------|-----------|--------------------------------|
| name         | Char      | رقم العقد (تلقائي)             |
| customer_id  | Many2one  | العميل (res.partner)           |
| car_id       | Many2one  | السيارة (rental.car)           |
| date_from    | Date      | تاريخ الاستلام                 |
| date_to      | Date      | تاريخ التسليم                  |
| total_days   | Integer   | عدد الأيام (محسوب تلقائياً)   |
| total_amount | Float     | المبلغ الإجمالي (محسوب تلقائياً)|
| state        | Selection | draft/confirmed/active/done/cancelled |
| note         | Text      | ملاحظات                        |

## التثبيت

### من واجهة الويب
1. **Settings → Activate Developer Mode**
2. **Apps → Update Apps List**
3. ابحث عن `Car Rental` وانقر **Install**

### من سطر الأوامر
```bash
python odoo-bin -d <your_database> -i car_rental --stop-after-init
```

### تحديث الوحدة
```bash
python odoo-bin -d <your_database> -u car_rental --stop-after-init
```

## الترخيص

LGPL-3

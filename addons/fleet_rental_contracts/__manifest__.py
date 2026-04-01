{
    "name": "Fleet Rental Contracts",
    "version": "1.0",
    "category": "Rental",
    "summary": "Comprehensive car rental contract management for Odoo 19.",
    "description": """
Car Rental Management
=====================
Full-featured car rental module covering:

- Rental Contracts (open / suspend / close / cancel / transfer to legal or insurance)
- Multi-branch operations with inter-branch delivery fees
- Customer profiles: individual, company, government entity
- Customer source tracking (app channels, direct branch)
- Configurable grace period for fee-free cancellation
- Flexible pricing plans: daily, weekly, monthly, hourly, 3-6-9-12-24-36 month subscriptions
- Scope pricing by branch, category, model, year, specific vehicle, or specific customer
- Extra KM / extra hours / open-KM / extra driver / deductible / delivery charges
- Insurance types: comprehensive, comprehensive without deductible, third-party
- Check-out and check-in checklists with photo attachments per item
- Traffic violations, parking violations and damage/misuse tracking
- Violation states: pending → charged / waived
- Vehicle status management (available, rented, maintenance, accident, total loss, etc.)
- Vehicle insurance details with expiry tracking
- Contract sequence numbering (RC/YYYY/XXXX)
- PDF contract report with financial summary and checklist
- Chatter & activity tracking on contracts
""",
    "depends": ["base", "mail", "fleet", "account"],
    "data": [
        "security/ir.model.access.csv",
        "data/rental_data.xml",
        "views/rental_branch_view.xml",
        "views/rental_pricing_view.xml",
        "views/rental_checklist_view.xml",
        "views/rental_contract_view.xml",
        "views/asset_view.xml",
        "views/rental_menu.xml",
        "reports/rental_contract_report.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}

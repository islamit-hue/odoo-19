from odoo import fields, models


class RentalBranch(models.Model):
    _name = "rental.branch"
    _description = "Rental Branch"
    _rec_name = "name"

    name = fields.Char(string="Branch Name", required=True)
    code = fields.Char(string="Branch Code")
    address = fields.Text(string="Address")
    city = fields.Char(string="City")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    manager_id = fields.Many2one("res.users", string="Branch Manager")
    active = fields.Boolean(default=True)
    notes = fields.Text(string="Notes")

    contract_ids = fields.One2many(
        "rental.contract", "branch_id", string="Contracts"
    )
    contract_count = fields.Integer(
        compute="_compute_contract_count", string="# Contracts"
    )

    def _compute_contract_count(self):
        for rec in self:
            rec.contract_count = len(rec.contract_ids)

    def action_view_contracts(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Contracts",
            "res_model": "rental.contract",
            "view_mode": "list,form",
            "domain": [("branch_id", "=", self.id)],
            "context": {"default_branch_id": self.id},
        }

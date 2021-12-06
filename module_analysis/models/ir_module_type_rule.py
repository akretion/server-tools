# Copyright (C) 2019-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class IrModuleType(models.Model):
    _name = "ir.module.type.rule"
    _description = "Modules Types Rules"
    _order = "sequence"

    sequence = fields.Integer(string="Sequence")

    module_domain = fields.Char(string="Module Domain", required=True, default="[]")

    module_type_id = fields.Many2one(
        string="Module type", comodel_name="ir.module.type", required=True
    )

    def _module_is_in_rule(self, module):
        self.ensure_one()
        domain = safe_eval(self.module_domain)
        if module.filtered_domain(domain):
            return True
        return False

    def _get_type_from_module(self, module):
        for rule in self.sorted("sequence"):
            if rule._module_is_in_rule(module):
                return rule.module_type_id

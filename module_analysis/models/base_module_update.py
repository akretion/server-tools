# Copyright (C) 2019-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BaseModuleUpdate(models.TransientModel):
    _inherit = "base.module.update"

    analyse_all_modules = fields.Boolean(
        string="Analyse Installed Modules", default=True
    )

    def update_module(self):
        return super(
            BaseModuleUpdate,
            self.with_context(analyse_all_modules=self.analyse_all_modules),
        ).update_module()

# Copyright 2020 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class MailMail(models.Model):
    _inherit = "mail.mail"

    def unlink(self):
        if self.env.context.get("confirm_auto_delete"):
            super().unlink()

    @api.model
    def vacuum_auto_deletes(self):
        mail_obj_delete = self.env["mail.mail"].with_context(
            {"confirm_auto_delete": True}
        )
        mail_obj_delete.search([("auto_delete", "=", True)]).unlink()

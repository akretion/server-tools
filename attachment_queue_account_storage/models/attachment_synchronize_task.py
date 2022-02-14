# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AttachmentSynchronizeTask(models.Model):
    _inherit = "attachment.synchronize.task"

    file_type = fields.Selection(
        selection_add=[
            ("account_move_import", "Account Move Import"),
            ("account_statement_import", "Account Statement Import"),
        ]
    )
    journal_id = fields.Many2one("account.journal")

    def _prepare_attachment_vals(self, data, filename):
        vals = super()._prepare_attachment_vals(data, filename)
        if self.journal_id:
            vals["journal_id"] = self.journal_id.id
        return vals

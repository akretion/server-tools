# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FetchmailAttachmentCondition(models.Model):
    _inherit = "fetchmail.attachment.condition"

    file_type = fields.Selection(
        selection_add=[
            ("account_move_import", "Account Move Import"),
        ]
    )
    journal_id = fields.Many2one("account.journal", check_company=True)

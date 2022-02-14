# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AttachmentQueue(models.Model):
    _inherit = "attachment.queue"

    file_type = fields.Selection(
        selection_add=[
            ("account_move_import", "Account Move Import"),
            ("account_statement_import", "Account Bank Statement Import"),
        ]
    )
    journal_id = fields.Many2one("account.journal")

    def _run(self):
        self.ensure_one()
        super()._run()
        if self.file_type == "account_move_import":
            vals = {
                "input_statement": self.datas,
                "file_name": self.name,
            }
            import_wizard_obj = self.env["credit.statement.import"]
            import_wizard = import_wizard_obj.with_context(
                active_model="account.journal", active_ids=[self.journal_id.id]
            ).create(vals)
            import_wizard.with_context(
                default_attachement_queue_id=self.id
            ).import_statement()
        elif self.file_type == "account_statement_import":
            import_wizard_obj = self.env["account.statement.import"]
            vals = {
                "statement_file": self.datas,
                "statement_filename": self.name,
            }
            import_wizard = import_wizard_obj.create(vals)
            import_wizard.import_file_button()

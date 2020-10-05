# @ 2016 Florian DA COSTA @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from odoo import api, models, fields
from .common import make_safe_filename


class AttachmentQueue(models.Model):
    _inherit = "attachment.queue"

    export_id = fields.Many2one("ir.exports")
    pattimpex_id = fields.Many2one(
        "patterned.import.export", string="Patterned Import/Export"
    )

    # Export part

    @api.onchange("task_id")
    def onchange_task_id(self):
        for attachment in self:
            if attachment.task_id.method_type == "export_pattimpex":
                attachment.file_type = "export_pattimpex"

    # Import part

    def import_using_pattern(self):
        wizard = self.env["import.pattern.wizard"].create(
            {
                "ir_exports_id": self.export_id.id,
                "import_file": self.datas,
                "name": make_safe_filename(self.name),
            }
        )
        self.pattimpex_id = wizard.action_launch_import()

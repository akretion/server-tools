# @ 2016 Florian DA COSTA @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from odoo import api, models, fields


class AttachmentQueue(models.Model):
    _inherit = "attachment.queue"

    task_id = fields.Many2one("attachment.synchronize.task", string="Task")
    method_type = fields.Selection(related="task_id.method_type")
    storage_backend_id = fields.Many2one(
        "storage.backend",
        string="Storage Backend",
        related="task_id.backend_id",
        store=True,
    )
    file_type = fields.Selection(
        selection_add=[("export_pattimpex", "Export File using patterns (External location)")]
    )
    export_id = fields.Many2one("ir.exports")
    pattimpex_id = fields.Many2one("patterned.import.export", string="Patterned Import/Export")

    # Export part

    def _run_export_pattimpex(self):
        path = os.path.join(self.task_id.filepath, self.datas_fname)
        self.storage_backend_id._add_b64_data(path, self.datas)

    def _run(self):
        super()._run()
        if self.file_type == "export_pattimpex":
            self._run_export_pattimpex()

    @api.onchange("task_id")
    def onchange_task_id(self):
        for attachment in self:
            if attachment.task_id.method_type == "export_pattimpex":
                attachment.file_type = "export_pattimpex"

    # Import part

    def import_using_pattern(self):
        wizard = self.env["import.pattern.wizard"].create({
            "ir_exports_id": self.export_id.id,
            "import_file": self.datas,
            "name": self.name
        })
        self.pattimpex_id = wizard.action_launch_import()

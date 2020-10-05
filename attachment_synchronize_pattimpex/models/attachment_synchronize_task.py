# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
import logging
import os
import json
import odoo
from odoo import api, fields, models, tools
from odoo.osv import expression

_logger = logging.getLogger(__name__)

from .common import make_safe_filename


class AttachmentSynchronizeTask(models.Model):
    _inherit = "attachment.synchronize.task"

    pattern_pattimpex = fields.Char(
        string="Selection Pattern", compute="_compute_pattern_pattimpex"
    )
    domain_pattimpex_export = fields.Char(
        string="Domain for filtering records to export", default="[]"
    )
    export_id = fields.Many2one("ir.exports", string="Export pattern")

    def _compute_pattern_pattimpex(self):
        for rec in self:
            if rec.export_id:
                rec.pattern_pattimpex = (
                    make_safe_filename(rec.export_id.name)
                    + "*."
                    + rec.export_id.export_format
                )

    @api.model
    def run_task_import_using_patterns_scheduler(self, domain=None):
        if domain is None:
            domain = []
        domain = expression.AND(
            [domain, [("method_type", "=", "import_pattimpex"), ("enabled", "=", True)]]
        )
        for task in self.search(domain):
            task.run_import_pattimpex()

    def _prepare_attachment_vals(self, data, filename, export_id=None):
        result = super()._prepare_attachment_vals(data, filename)
        if export_id:
            result["export_id"] = export_id
        return result

    def run_import_pattimpex(self):
        """
        Similar copy of run_import, except :
        - uses self.pattern_pattimpex instead of self.pattern
        - on the resulting attachment.queues, runs import_using_pattern()
          which launches the pattern-import-export flow
        """
        self.ensure_one()
        attach_obj = self.env["attachment.queue"]
        backend = self.backend_id
        filepath = self.filepath or ""
        filenames = backend._list(
            relative_path=filepath, pattern=self.pattern_pattimpex
        )
        if self.avoid_duplicated_files:
            filenames = self._file_to_import(filenames)
        total_import = 0
        new_attachments = self.env["attachment.queue"]
        for file_name in filenames:
            with api.Environment.manage():
                with odoo.registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    try:
                        full_absolute_path = os.path.join(filepath, file_name)
                        data = backend._get_b64_data(full_absolute_path)
                        attach_vals = self._prepare_attachment_vals(
                            data, file_name, self.export_id.id
                        )
                        attachment = attach_obj.with_env(new_env).create(attach_vals)
                        new_full_path = False
                        if self.after_import == "rename":
                            new_name = self._template_render(self.new_name, attachment)
                            new_full_path = os.path.join(filepath, new_name)
                        elif self.after_import == "move":
                            new_full_path = os.path.join(self.move_path, file_name)
                        elif self.after_import == "move_rename":
                            new_name = self._template_render(self.new_name, attachment)
                            new_full_path = os.path.join(self.move_path, new_name)
                        if new_full_path:
                            backend._add_b64_data(new_full_path, data)
                        if self.after_import in (
                            "delete",
                            "rename",
                            "move",
                            "move_rename",
                        ):
                            backend._delete(full_absolute_path)
                        total_import += 1
                        new_attachments += attachment
                    except Exception as e:
                        new_env.cr.rollback()
                        raise e
                    else:
                        new_env.cr.commit()
                        attachment.import_using_pattern()
        _logger.info(
            "Run patterned import complete! Imported {0} files".format(total_import)
        )

    def run_export_pattimpex(self):
        for task in self.filtered(lambda r: r.export_id):
            new_ctx = {
                "active_ids": self.env[task.export_id.model].search(
                    json.loads(task.domain_pattimpex_export)
                )
            }
            wizard = self.env["export.pattern.wizard"].create(
                {"model": self.export_id.model.id, "ir_exports_id": self.export_id.id,}
            )
            pattimpex = wizard.with_context(new_ctx).action_launch_export()
            self.env["attachment.queue"].create(
                {"attachment_id": pattimpex.attachment_id.id, "file_type": "export"}
            )
            task.attachment_ids.filtered(lambda a: a.state == "pending").run()

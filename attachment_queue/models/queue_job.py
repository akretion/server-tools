# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models

from odoo.addons.queue_job.job import CANCELLED


class QueueJob(models.Model):
    _inherit = "queue.job"

    def _attachment_queues(self):
        """Return the attachment queues processed by the job (if any)"""
        self.ensure_one()
        if self.model_name != "attachment.queue" or self.method_name != "run_as_job":
            return self.env["attachment.queue"]
        return self.records.sudo().exists().filtered(lambda att: att.state != "done")

    def _message_failed_job(self):
        res = super()._message_failed_job()
        # The attachment is not flagged as failed by the job itself (a retryable
        # error would report a failure that is going to be retried): report it only
        # when the job is definitively failed.
        attachments = self._attachment_queues()
        if attachments:
            attachments._set_attachment_failure(self.exc_message or self.exc_name)
        return res

    def _change_job_state(self, state, result=None):
        res = super()._change_job_state(state, result=result)
        if state == CANCELLED:
            for job in self:
                # No job is left to process the attachment nor to report a failure:
                # the attachment would stay pending forever.
                attachments = job._attachment_queues()
                if attachments:
                    attachments.write(
                        {"state": "failed", "state_message": _("Job cancelled")}
                    )
        return res

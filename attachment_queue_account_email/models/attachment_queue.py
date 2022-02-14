# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AttachmentQueue(models.Model):
    _inherit = "attachment.queue"

    @api.model
    def _get_attachment_queue_data(self, condition, msg, att):
        res = super()._get_attachment_queue_data(condition, msg, att)
        if condition.journal_id:
            res["journal_id"] = condition.journal_id.id
        return res

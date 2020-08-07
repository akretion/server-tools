# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    attachement_queue_id = fields.Many2one(
        'attachment.queue'
        )


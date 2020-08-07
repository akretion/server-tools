# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    attachement_queue_id = fields.Many2one(
        'attachment.queue'
    )

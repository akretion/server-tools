# coding: utf-8
#   @author Sébastien BEAU @ Akretion
#   @author Florian DA COSTA @ Akretion
#   @author Benoit GUILLOT @ Akretion
#   @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class FetchmailAttachmentCondition(models.Model):
    _inherit = 'fetchmail.attachment.condition'

    file_type = fields.Selection(
        selection_add=[
            ('account_move_import', 'Account Move Import'),
            ('account_statement_import', 'Account Statement Import')
        ])
    journal_id = fields.Many2one('account.journal')

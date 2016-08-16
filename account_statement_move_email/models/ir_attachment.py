# coding: utf-8
#   @author Sébastien BEAU @ Akretion
#   @author Florian DA COSTA @ Akretion
#   @author Benoit GUILLOT @ Akretion
#   @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class IrAttachmentMetadata(models.Model):
    _inherit = "ir.attachment.metadata"

    @api.model
    def _get_attachment_metadata_data(self, condition, msg, att):
        res = super(IrAttachmentMetadata, self)._get_attachment_metadata_data(
            condition, msg, att)
        if condition.journal_id:
            res['journal_id'] = condition.journal_id.id
        return res

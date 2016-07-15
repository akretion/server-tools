# coding: utf-8
# @ 2016 Florian DA COSTA @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class IrAttachmentMetadata(models.Model):
    _inherit = 'ir.attachment.metadata'

    task_id = fields.Many2one('external.file.task', string='Task')
    location_id = fields.Many2one(
        'external.file.location', string='Location',
        related='task_id.location_id', store=True)
    file_type = fields.Selection(
        selection_add=[
            ('export_external_location',
             'Export File (External location)')
        ])


    @api.multi
    def _run(self):
        super(IrAttachmentMetadata, self)._run()
        if self.file_type == 'export_external_location':
            # TODO
            pass

# -*- coding: utf-8 -*-
###############################################################################
#
#   account_statement_repository for OpenERP
#   Copyright (C) 2013 Akretion (http://www.akretion.com). All Rights Reserved
#   @author Benoît GUILLOT <benoit.guillot@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, api, fields
import os


class IrAttachmentMetadata(models.Model):
    _inherit = "ir.attachment.metadata"

    file_type = fields.Selection(
        selection_add=[
            ('account_move_import', 'Account Move Import'),
            ('account_statement_import', 'Account Statement Import')
        ])
    journal_id = fields.Many2one(
        'account.journal'
        )

    @api.multi
    def _run(self):
        self.ensure_one()
        super(IrAttachmentMetadata, self)._run()
        attach_obj = self.pool['ir.attachment']
        if self.file_type == 'account_move_import':
            vals = {
                'input_statement': self.datas,
                'file_name': self.datas_fname,
            }
            import_wizard_obj = self.env['credit.statement.import']
            import_wizard = import_wizard_obj.with_context(
                active_model='account.journal',
                active_ids=[self.journal_id.id]).create(vals)
            import_wizard.with_context(
                default_attachement_metadata_id=self.id).import_statement()
        elif self.file_type == 'account_statement_import':
            journal_id = self.env.context.get('journal_id', False)
            import_wizard_obj = self.env['account.bank.statement.import']
            vals = {
                'data_file': self.datas,
            }
            import_wizard = import_wizard_obj.create(vals)
            import_wizard.with_context(
                journal_id=self.journal_id.id,
                default_attachement_metadata_id=self.id).import_file()

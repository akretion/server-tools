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

from openerp import models, fields, api


class ExternalFileTask(models.Model):
    _inherit = 'external.file.task'

    file_type = fields.Selection(
        selection_add=[
            ('account_move_import', 'Account Move Import'),
            ('account_statement_import', 'Account Statement Import')
        ])
    journal_id = fields.Many2one(
        'account.journal'
        )

    @api.multi
    def _prepare_attachment_vals(self, datas, filename, md5_datas):
        self.ensure_one()
        res = super(ExternalFileTask, self)._prepare_attachment_vals(
            datas, filename, md5_datas)
        if self.journal_id:
            res['journal_id'] = self.journal_id.id
        return res

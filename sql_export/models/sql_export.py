# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Akretion (<http://www.akretion.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class SqlExport(models.Model):
    _name = "sql.export"
    _inherit = ['sql.request.mixin']
    _description = "SQL export"

    _sql_request_groups_relation = 'groups_sqlquery_rel'

    _sql_request_users_relation = 'users_sqlquery_rel'

    _check_execution_enabled = False

    copy_options = fields.Char(
        string='Copy Options', required=False,
        default="CSV HEADER DELIMITER ';'")
    file_format = fields.Selection(
        [('csv', 'CSV')],
        default='csv',
        required=True)
    field_ids = fields.Many2many(
        'ir.model.fields',
        'fields_sqlquery_rel',
        'sql_id',
        'field_id',
        'Parameters',
        domain=[('model', '=', 'sql.file.wizard')])

    encoding = fields.Selection(
        [('utf-8', 'utf-8'), ('utf-16', 'utf-16'),
         ('windows-1252', 'windows-1252'), ('latin1', 'latin1'),
         ('latin2', 'latin2'), ('big5', 'big5'), ('gb18030', 'gb18030'),
         ('shift_jis', 'shift_jis'), ('windows-1251', 'windows-1251'),
         ('koir8_r', 'koir8_r')], string='Encoding', required=True,
        default='utf-8')

    @api.multi
    def export_sql_query(self):
        self.ensure_one()
        wiz = self.env['sql.file.wizard'].create({
            'sql_export_id': self.id})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sql.file.wizard',
            'res_id': wiz.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self._context,
            'nodestroy': True,
        }

    @api.multi
    def _get_file_extension(self):
        self.ensure_one()
        if self.file_format == 'csv':
            return 'csv'

    @api.multi
    def csv_get_datas_from_query(self, variable_dict):
        self.ensure_one()
        # Execute Request
        res = self._execute_sql_request(
            params=variable_dict, mode='stdout',
            copy_options=self.copy_options)
        if self.encoding:
            res = res.encode(self.encoding)
        return res

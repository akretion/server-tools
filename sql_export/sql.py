# -*- coding: utf-8 -*-
###############################################################################
#
#   action_server_email for OpenERP
#   Copyright (C) 2013-TODAY Akretion <http://www.akretion.com>.
#   @author Florian DA COSTA <florian.dacosta@akretion.com>
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

from openerp.osv.orm import Model
from openerp.osv import fields, orm
from openerp.tools.translate import _
import StringIO
import csv
import base64
import time


PROHIBITED_WORDS = ['delete', 'drop', 'insert', 'alter', 'truncate', 'execute']


class SqlExport(Model):

    _name = "sql.export"

    _description = "SQL export"


    def _check_query(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if any(word in obj.query.lower() for word in PROHIBITED_WORDS):
                return False
            if obj.query.split(' ')[0].lower() != 'select':
                return False
        return True


    _columns = {
        'name': fields.char('Name', required=True),
        'query': fields.text('Query', required=True, help="You can't use the following word : delete, drop, create, insert, update, alter, truncate, execute"),
        'group_ids': fields.many2many('res.groups', 'groups_sqlquery_rel', 'sql_id', 'group_id', 'Allowed Groups'),
        'user_ids': fields.many2many('res.users', 'users_sqlquery_rel', 'sql_id', 'user_id', 'Allowed Users'),
    }


    _constraints = [(_check_query, 'The query you want make is not allowed : prohibited actions (Delete, drop...)', ['query'])]


    def export_sql_query(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        for obj in self.browse(cr, uid, ids, context=context):
            cr.execute(obj.query)
            results = cr.dictfetchall()
            if results:
                header = results[0].keys()
                values = [x.values() for x in results]
            else:
                raise orm.except_orm(_("No data"),
                                     _("The query did not return any data."))
            now = time.strftime('%Y-%m-%d',time.localtime())
            output = StringIO.StringIO()
            writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(header)
            for value in values:
                value_encode = [x.encode('utf-8') for x in value if isinstance(x, unicode)]
                writer.writerow(value_encode)
            output.getvalue()
            new_output = base64.b64encode(output.getvalue())
            output.close()
            wiz = self.pool.get('sql.file.wizard').create(cr, uid, {'file': new_output, 'file_name': obj.name + '_' + now + '.csv'})
            cr.commit()
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sql.file.wizard',
            'res_id': wiz,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'nodestroy': True,
        }


    def write(self, cr, uid, ids, vals, context=None):
        if vals:
            if 'query' in vals:
                try:
                    cr.execute(vals['query'])
                except:
                    raise orm.except_orm(_("Invalid Query"),
                                         _("The Sql query is not valid."))
        return super(SqlExport, self).write(cr, uid, ids, vals, context=context)


    def create(self, cr, uid, vals, context=None):
        if vals:
            if 'query' in vals:
                try:
                    cr.execute(vals['query'])
                except:
                    raise orm.except_orm(_("Invalid Query"),
                                         _("The Sql query is not valid."))
        return super(SqlExport, self).create(cr, uid, vals, context=context)


